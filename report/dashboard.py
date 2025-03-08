from fasthtml.common import *
import matplotlib.pyplot as plt
from employee_events import Employee, Team
from utils import load_model
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable,
)
from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(None, model)

    def component_data(self, entity_id, model):
        names_data = model.names()
        return [(row[0], row[1]) for row in names_data.itertuples(index=False)]


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        df = model.username(entity_id)
        if "full_name" in df.columns:
            name = df.iloc[0]["full_name"]
        elif "team_name" in df.columns:
            name = df.iloc[0]["team_name"]
        else:
            name = "Unknown"
        return H1(name)


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        data = model.event_counts(entity_id).fillna(0)
        data = data.set_index("event_date").sort_index().cumsum()
        data.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        data.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        ax.set_title("Cumulative Event Trends")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Events")

        return fig


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        pred_proba = self.predictor.predict_proba(data)

        pred = (
            pred_proba[:, 1].mean() if model.name == "team" else pred_proba[0][1]
        )

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        return fig


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id).rename(
            columns={"note_date": "Date", "note": "Note"}
        )


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
            selected="Employee",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


class Report(CombinedComponent):
    children = [DashboardFilters(), Header(), Visualizations(), NotesTable()]


app = FastHTML()
report = Report()


@app.get("/")
def index():
    return report(1, Employee())


@app.get("/employee/{entity_id}")
def employee_route(entity_id: int):
    try:
        employee = Employee()
        employee_data = employee.username(entity_id)
        if employee_data.empty:
            return "Employee not found"
        return report(entity_id, Employee())
    except Exception as e:
        print(f"Error fetching employee data: {e}")
        return "Internal Server Error", 500


@app.get("/team/{entity_id}")
def team_route(entity_id: int):
    try:
        team = Team()
        team_data = team.username(entity_id)
        if team_data.empty:
            return "Team not found"
        return report(entity_id, Team())
    except Exception as e:
        print(f"Error fetching team data: {e}")
        return "Internal Server Error", 500


@app.get("/update_dropdown")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print("PARAM", r.query_params["profile_type"])

    if r.query_params["profile_type"] == "Team":
        return dropdown(None, Team())
    elif r.query_params["profile_type"] == "Employee":
        return dropdown(None, Employee())


@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse

    data = await r.form()
    profile_type = data._dict["profile_type"]
    entity_id = int(data._dict["user-selection"])

    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{entity_id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{entity_id}", status_code=303)


serve()
