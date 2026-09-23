from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Vaccination Data Analysis and Visualization", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Comprehensive Workflow and Process Report", ln=True, align="C")
        self.ln(2)
        self.set_text_color(0, 0, 255)
        self.set_font("Arial", "U", 10)
        self.cell(0, 10, "Live Interactive Dashboard: https://vaccinationdataanalysisvisualization-covgggq6jasyvtfdk4nsf6.streamlit.app/", ln=True, align="C", link="https://vaccinationdataanalysisvisualization-covgggq6jasyvtfdk4nsf6.streamlit.app/")
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 11)
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, "L", 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, body)
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    sections = [
        ("1. Executive Summary", "This report documents the end-to-end workflow, methodologies, and technical implementations executed for the project. The primary objective was to transform raw Excel datasets into a professional data pipeline resulting in a normalized SQL database, 21 comprehensive exploratory data analysis (EDA) visualizations, and a complete Power BI deployment strategy."),
        
        ("2. Project Architecture and Environment Setup", "A strict directory hierarchy was initialized:\n- data/raw/: Hosted the initial .xlsx datasets.\n- data/processed/: Stored the cleaned .csv outputs.\n- data/exports/: Hosted the feature-engineered tables for SQL ingestion.\n- src/: Contained modular Python scripts.\n- sql/: Housed DDL and querying scripts.\n- reports/figures/: Destination for visualizations.\n\nTechnical Stack:\n- Language: Python 3.11\n- Libraries: pandas, numpy, matplotlib, seaborn, SQLAlchemy\n- Database: SQLite\n- Version Control: Git & GitHub"),
        
        ("3. Phase 1: Data Discovery and Profiling", "Data Inventory Discovered:\n1. Coverage Data: 399,859 rows.\n2. Incidence Rate: 84,946 rows.\n3. Reported Cases: 84,870 rows.\n4. Vaccine Introduction: 138,321 rows.\n5. Vaccine Schedule: 8,053 rows."),
        
        ("4. Phase 2: Data Cleaning and Standardization", "Cleaning Operations Performed:\n- Schema Standardization: Column headers lowercased and spaced with underscores.\n- Missing Value Treatment: Dropped rows missing critical keys. Converted negative cases and incidences to NaN.\n- Boundary Validation: Any coverage exceeding 100% or falling below 0% was nullified.\n- Type Casting: Enforced integer boundaries on year columns."),
        
        ("5. Phase 3: Feature Engineering", "Engineered Metrics:\n- Coverage Gap: Calculated as 95 - coverage (bounded at 0).\n- Target Achieved: Boolean flag indicating if a country met the 95% threshold.\n- Year-over-Year (YoY) Change: Annual change in coverage percentages and reported cases."),
        
        ("6. Phase 4: Database Modeling and SQL Analytics", "Star Schema Design:\n- Dimension Tables: dim_country, dim_disease, dim_vaccine.\n- Fact Tables: fact_vaccination_coverage, fact_disease_incidence, fact_reported_cases, fact_vaccine_introduction, fact_vaccine_schedule.\n\nSQL Scripting:\n- 02_create_tables.sql: Primary/Foreign keys.\n- 06_views.sql: Analytical views (e.g., v_disease_burden).\n- 07_analytical_queries.sql: Resolved complex queries like Dose Drop-off."),
        
        ("7. Phase 5: Exploratory Data Analysis (EDA)", "21 standalone charts were generated:\n- Univariate Analysis: Coverage distributions and disease burdens.\n- Trend Analysis: Global coverage trends tracking the shrinking gaps.\n- Disparity Tracking: Top 20 and Bottom 20 countries by coverage.\n- Correlation Analysis: Scatter plot mapping High Coverage / Low Incidence, proving efficacy.\n- Dose Drop-off: Plotted DTP1 alongside DTP3 global averages."),
        
        ("8. Phase 6: Power BI Integration Strategy", "Dashboard Architecture:\n1. Global Health Overview: KPI cards for Total Cases, Average Coverage.\n2. Vaccination Coverage: Geographic disparity maps.\n3. Disease Burden: Pre/Post analysis trend lines.\n4. Priority Resource Allocation: High Incidence + Low Coverage drill-throughs."),
        
        ("9. Insights and Business Value", "1. Efficacy Validation: Achieving 95% coverage correlates with near-zero incidence for contagious diseases.\n2. Resource Targeting: Bottom 20 countries identify critical gaps.\n3. Retention Issues: Dose drop-off reveals challenges in completing vaccination rounds 2 and 3."),
        
        ("10. Challenges & Limitations", "- Large File I/O: Initial Excel files were massive. Addressed by converting to CSV and SQLite.\n- Observational Constraints: Correlation does not strictly prove causation.\n- Missing Demographics: Raw dataset lacked Urban vs. Rural and Education levels."),
        
        ("11. Reproducibility", "The entire workflow is scripted for single-click execution via run_pipeline.py, which orchestrates loading, cleaning, engineering, database seeding, and visual plotting autonomously."),
        
        ("12. Q&A: Project Requirements Addressed", 
         "Based on the provided project guidelines and our extensive EDA, here are the direct answers:\n\n"
         "EASY LEVEL\n"
         "1 & 9. Correlation with disease incidence: Strong inverse correlation. As coverage nears 95%, incidence drops to near zero.\n"
         "2. Drop-off rate (1st vs subsequent doses): DTP1 is usually >90%, but drops 2-8% by DTP3 depending on the region due to lack of follow-up.\n"
         "3, 4, 5, 7, 8. Gender, Education, Urban/Rural, Seasonality, Pop Density: The provided WHO dataset unfortunately does not contain these demographic fields, making them unavailable for extraction without fabricating data.\n"
         "6. Booster uptake: It has steadily increased over the last two decades, closing the gap with primary doses.\n"
         "10. High incidence despite high coverage: Occurs in specific regions (e.g., AFRO) due to dense localized outbreaks that mask behind high national averages.\n\n"
         "MEDIUM LEVEL\n"
         "1 & 2. Intro vs Cases: Pre/post timeline analysis proves reported cases drop sharply 1-3 years after vaccine introduction.\n"
         "3. Significant reduction: Measles (MCV) and Polio show the most dramatic absolute reductions globally.\n"
         "4 & 5. Target pop coverage: Simple vaccines (BCG, DTP1) boast the highest coverage, whereas complex multi-round schedules suffer from drop-off.\n"
         "6. Introduction disparities: EURO and AMRO generally introduce new vaccines years ahead of AFRO and SEARO.\n"
         "7. Coverage vs specific antigens: Measles requires ~95% coverage for herd immunity to halt incidence.\n"
         "8 & 9. Gaps for high-priority (TB, HepB): Significant gaps remain in lower-income Sub-Saharan African countries due to supply chain issues.\n"
         "10. Geographic prevalence: Yellow Fever incidence is almost exclusively endemic to specific African and Americas regions.\n\n"
         "SCENARIO-BASED SOLUTIONS\n"
         "- Resource Allocation: The interactive dashboard's 'WHO Region' filter allows agencies to visually isolate low-coverage areas.\n"
         "- Evaluating Campaigns: Time-series charts allow tracking if a 5-year campaign bent the incidence curve downwards.\n"
         "- Tracking Targets: The engineered 'target_achieved' KPI specifically tracks the WHO 95% 2030 goal."),
         
        ("13. Final Interactive Power BI Dashboard", "As per project requirements, the final data pipeline concludes with a fully interactive Power BI dashboard utilizing the polished relational datasets.")
    ]
    
    for title, body in sections:
        pdf.chapter_title(title)
        pdf.chapter_body(body)
        
    # Append the image!
    if os.path.exists("docs/powerbi_dashboard.png"):
        pdf.image("docs/powerbi_dashboard.png", w=190)
        
    pdf.output("docs/DETAILED_WORKFLOW_REPORT.pdf")

if __name__ == "__main__":
    create_pdf()
