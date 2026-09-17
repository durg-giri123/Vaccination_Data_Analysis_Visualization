import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EDA:
    def __init__(self, data_dir: str = "../data/exports"):
        self.data_dir = Path(data_dir)
        self.figures_dir = Path(__file__).parent.parent / "reports" / "figures"
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.data = {}
        
    def load_data(self):
        for file in self.data_dir.glob("*.csv"):
            name = file.stem
            self.data[name] = pd.read_csv(file)
            logging.info(f"Loaded {name}")
            
    def generate_visualizations(self):
        sns.set_theme(style="whitegrid")
        df_cov = self.data.get('coverage_engineered')
        df_inc = self.data.get('incidence_engineered')
        df_cases = self.data.get('cases_engineered')
        df_intro = self.data.get('intro_engineered')
        df_sched = self.data.get('schedule_engineered')

        if df_cov is not None:
            # 1 to 6 as before
            plt.figure(figsize=(10,6))
            global_trend = df_cov.groupby('year')['coverage'].mean().reset_index()
            sns.lineplot(data=global_trend, x='year', y='coverage', marker='o')
            plt.title("1. Global Average Vaccination Coverage Trend")
            plt.savefig(self.figures_dir / "01_global_coverage_trend.png", bbox_inches='tight')
            plt.close()

            plt.figure(figsize=(10,6))
            sns.histplot(df_cov['coverage'].dropna(), bins=20, kde=True)
            plt.title("2. Distribution of Vaccination Coverage")
            plt.savefig(self.figures_dir / "02_coverage_distribution.png", bbox_inches='tight')
            plt.close()

            recent_year = df_cov['year'].max()
            recent_cov = df_cov[df_cov['year'] == recent_year].groupby('name')['coverage'].mean().sort_values()
            plt.figure(figsize=(12,8))
            recent_cov.tail(20).plot(kind='barh', color='steelblue')
            plt.title(f"3. Top 20 Countries by Avg Coverage ({recent_year})")
            plt.savefig(self.figures_dir / "03_top_20_countries_coverage.png", bbox_inches='tight')
            plt.close()
            
            plt.figure(figsize=(12,8))
            recent_cov.head(20).plot(kind='barh', color='darkred')
            plt.title(f"4. Bottom 20 Countries by Avg Coverage ({recent_year})")
            plt.savefig(self.figures_dir / "04_bottom_20_countries_coverage.png", bbox_inches='tight')
            plt.close()

            if 'group' in df_cov.columns:
                plt.figure(figsize=(12,6))
                sns.boxplot(data=df_cov[df_cov['year'] == recent_year], x='group', y='coverage')
                plt.xticks(rotation=45)
                plt.title(f"5. Regional Coverage Comparison ({recent_year})")
                plt.savefig(self.figures_dir / "05_regional_coverage_comparison.png", bbox_inches='tight')
                plt.close()
                
                plt.figure(figsize=(12,6))
                trend_reg = df_cov.groupby(['year', 'group'])['coverage'].mean().reset_index()
                sns.lineplot(data=trend_reg, x='year', y='coverage', hue='group')
                plt.title("6. Regional Coverage Trend Over Time")
                plt.savefig(self.figures_dir / "06_regional_coverage_trend.png", bbox_inches='tight')
                plt.close()

            plt.figure(figsize=(10,6))
            gap_trend = df_cov.groupby('year')['coverage_gap'].mean().reset_index()
            sns.lineplot(data=gap_trend, x='year', y='coverage_gap', color='red', marker='o')
            plt.title("7. Average Coverage Gap to 95% Target Over Time")
            plt.savefig(self.figures_dir / "07_coverage_gap_trend.png", bbox_inches='tight')
            plt.close()

            plt.figure(figsize=(12,8))
            antigen_cov = df_cov[df_cov['year'] == recent_year].groupby('antigen')['coverage'].mean().sort_values(ascending=False).head(20)
            antigen_cov.plot(kind='bar', color='darkgreen')
            plt.title(f"8. Average Coverage by Antigen (Top 20, {recent_year})")
            plt.savefig(self.figures_dir / "08_coverage_by_antigen.png", bbox_inches='tight')
            plt.close()

            dtp = df_cov[df_cov['antigen'].isin(['DTP1', 'DTP3'])]
            if not dtp.empty:
                plt.figure(figsize=(10,6))
                sns.lineplot(data=dtp, x='year', y='coverage', hue='antigen', marker='o')
                plt.title("9. Dose Drop-off: DTP1 vs DTP3 Global Trend")
                plt.savefig(self.figures_dir / "09_dose_dropoff.png", bbox_inches='tight')
                plt.close()

            measles = df_cov[df_cov['antigen'].str.contains('MCV', na=False, case=False)]
            if not measles.empty:
                plt.figure(figsize=(10,6))
                sns.lineplot(data=measles, x='year', y='coverage', hue='antigen', marker='o')
                plt.axhline(95, ls='--', color='red', label='95% Target')
                plt.title("10. Measles 95% Target Tracking")
                plt.legend()
                plt.savefig(self.figures_dir / "10_measles_target_tracking.png", bbox_inches='tight')
                plt.close()
                
            plt.figure(figsize=(10,6))
            target_ach = df_cov.groupby('year')['target_achieved'].mean().reset_index()
            sns.lineplot(data=target_ach, x='year', y='target_achieved', color='blue')
            plt.title("11. % of Records Achieving 95% Target")
            plt.savefig(self.figures_dir / "11_target_achieved_pct.png", bbox_inches='tight')
            plt.close()

        if df_inc is not None:
            plt.figure(figsize=(10,6))
            inc_trend = df_inc.groupby('year')['incidence_rate'].mean().reset_index()
            sns.lineplot(data=inc_trend, x='year', y='incidence_rate', marker='o', color='purple')
            plt.title("12. Global Disease Incidence Trend")
            plt.savefig(self.figures_dir / "12_disease_incidence_trend.png", bbox_inches='tight')
            plt.close()

            plt.figure(figsize=(12,6))
            disease_inc = df_inc.groupby('disease')['incidence_rate'].mean().sort_values(ascending=False).head(10)
            disease_inc.plot(kind='bar', color='purple')
            plt.title("13. Average Incidence Rate by Disease (Top 10)")
            plt.savefig(self.figures_dir / "13_incidence_by_disease.png", bbox_inches='tight')
            plt.close()

        if df_cases is not None:
            plt.figure(figsize=(10,6))
            cases_trend = df_cases.groupby('year')['cases'].sum().reset_index()
            sns.lineplot(data=cases_trend, x='year', y='cases', marker='o', color='orange')
            plt.title("14. Global Reported Cases Trend")
            plt.savefig(self.figures_dir / "14_reported_cases_trend.png", bbox_inches='tight')
            plt.close()

            plt.figure(figsize=(12,6))
            disease_cases = df_cases.groupby('disease')['cases'].sum().sort_values(ascending=False).head(10)
            disease_cases.plot(kind='bar', color='orange')
            plt.title("15. Total Reported Cases by Disease (Top 10)")
            plt.savefig(self.figures_dir / "15_cases_by_disease.png", bbox_inches='tight')
            plt.close()
            
            plt.figure(figsize=(12,6))
            recent_year = df_cases['year'].max()
            disease_cases_recent = df_cases[df_cases['year']==recent_year].groupby('disease')['cases'].sum().sort_values(ascending=False).head(10)
            disease_cases_recent.plot(kind='pie', autopct='%1.1f%%')
            plt.title(f"16. Cases Distribution by Disease ({recent_year})")
            plt.savefig(self.figures_dir / "16_cases_pie.png", bbox_inches='tight')
            plt.close()

        if df_intro is not None:
            plt.figure(figsize=(10,6))
            intro_trend = df_intro[df_intro['intro'] == 'Introduced'].groupby('year').size()
            intro_trend.plot(kind='line', marker='o', color='teal')
            plt.title("17. Vaccine Introductions Over Time")
            plt.savefig(self.figures_dir / "17_vaccine_intro_timeline.png", bbox_inches='tight')
            plt.close()

        if df_cov is not None and df_inc is not None:
            cov_agg = df_cov.groupby(['code', 'year'])['coverage'].mean().reset_index()
            inc_agg = df_inc.groupby(['code', 'year'])['incidence_rate'].mean().reset_index()
            merged_inc = pd.merge(cov_agg, inc_agg, on=['code', 'year'])

            plt.figure(figsize=(10,6))
            sns.scatterplot(data=merged_inc, x='coverage', y='incidence_rate', alpha=0.5)
            plt.title("18. Vaccination Coverage vs Average Incidence Rate")
            plt.yscale('log')
            plt.savefig(self.figures_dir / "18_coverage_vs_incidence.png", bbox_inches='tight')
            plt.close()

            recent_merged = merged_inc[merged_inc['year'] >= 2018].groupby('code').mean().reset_index()
            plt.figure(figsize=(10,6))
            sns.scatterplot(data=recent_merged, x='coverage', y='incidence_rate')
            plt.axvline(90, ls='--', color='gray')
            plt.axhline(recent_merged['incidence_rate'].median(), ls='--', color='gray')
            plt.title("19. Quadrant Analysis: Coverage vs Incidence (Recent Years)")
            plt.yscale('log')
            plt.savefig(self.figures_dir / "19_quadrant_analysis.png", bbox_inches='tight')
            plt.close()

        if df_cov is not None and df_cases is not None:
            cov_agg = df_cov.groupby(['code', 'year'])['coverage'].mean().reset_index()
            cases_agg = df_cases.groupby(['code', 'year'])['cases'].sum().reset_index()
            merged_cases = pd.merge(cov_agg, cases_agg, on=['code', 'year'])

            plt.figure(figsize=(10,6))
            sns.scatterplot(data=merged_cases, x='coverage', y='cases', alpha=0.5, color='green')
            plt.title("20. Vaccination Coverage vs Reported Cases")
            plt.yscale('log')
            plt.savefig(self.figures_dir / "20_coverage_vs_cases.png", bbox_inches='tight')
            plt.close()
            
            # 21 Correlation heatmap
            plt.figure(figsize=(8,6))
            sns.heatmap(merged_cases[['coverage', 'cases']].corr(), annot=True, cmap='coolwarm')
            plt.title("21. Correlation: Coverage vs Cases")
            plt.savefig(self.figures_dir / "21_correlation_heatmap.png", bbox_inches='tight')
            plt.close()

    def run_all(self):
        self.load_data()
        self.generate_visualizations()
        logging.info("EDA completed successfully.")

if __name__ == "__main__":
    eda = EDA()
    eda.run_all()
