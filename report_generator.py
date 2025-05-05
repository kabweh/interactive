import os
import datetime
from typing import Dict, List, Any, Optional
import jinja2
import weasyprint

class ReportGenerator:
    """
    Generates progress reports for the AI Tutor application.
    """
    
    def __init__(self, report_folder: str = "static/reports", template_folder: str = "templates"):
        """
        Initialize the report generator.
        
        Args:
            report_folder: Directory to store generated reports
            template_folder: Directory containing report templates
        """
        self.report_folder = report_folder
        self.template_folder = template_folder
        
        # Create folders if they don't exist
        os.makedirs(report_folder, exist_ok=True)
        os.makedirs(template_folder, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_folder),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self) -> None:
        """Create default HTML templates for reports if they don't exist."""
        html_template_path = os.path.join(self.template_folder, "progress_report.html")
        if not os.path.exists(html_template_path):
            with open(html_template_path, 'w') as f:
                f.write(DEFAULT_HTML_TEMPLATE)
    
    def generate_html_report(self, report_data: Dict) -> str:
        """
        Generate an HTML progress report.
        
        Args:
            report_data: Dictionary containing report data
        
        Returns:
            Path to the generated HTML report
        """
        # Populate defaults
        report_data.setdefault('report_title', 'Student Progress Report')
        report_data.setdefault('student_name', 'Student')
        report_data.setdefault('report_period', 'Last 30 days')
        report_data.setdefault('generation_date', datetime.datetime.now().strftime('%B %d, %Y'))
        report_data.setdefault('overall_progress', 'Good')
        report_data.setdefault('total_quizzes', 0)
        report_data.setdefault('average_score', 0)
        report_data.setdefault('quiz_results', [])
        report_data.setdefault('improvement_areas', [])
        report_data.setdefault('trend_description', 'remained consistent')
        report_data.setdefault('trend_period', 'month')
        report_data.setdefault('current_year', datetime.datetime.now().year)
        
        template = self.jinja_env.get_template('progress_report.html')
        html_content = template.render(**report_data)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"progress_report_{report_data['student_name'].replace(' ', '_').lower()}_{timestamp}.html"
        file_path = os.path.join(self.report_folder, filename)
        with open(file_path, 'w') as f:
            f.write(html_content)
        return file_path
    
    def generate_pdf_report(self, report_data: Dict) -> str:
        """
        Generate a PDF progress report.
        """
        html_path = self.generate_html_report(report_data)
        pdf_path = html_path.replace('.html', '.pdf')
        html = weasyprint.HTML(filename=html_path)
        html.write_pdf(pdf_path)
        return pdf_path
    
    def prepare_report_data(self, user_data: Dict, quiz_attempts: List[Dict], 
                           questions_data: Optional[Dict] = None) -> Dict:
        """
        Prepare data for a progress report.
        """
        report_data = {
            'report_title': f"Progress Report for {user_data.get('username', 'Student')}",
            'student_name': user_data.get('username', 'Student'),
            'report_period': 'Last 30 days',
            'generation_date': datetime.datetime.now().strftime('%B %d, %Y'),
            'total_quizzes': len(quiz_attempts),
            'current_year': datetime.datetime.now().year,
            'quiz_results': [],
            'improvement_areas': []
        }
        
        # Average score calculation
        if quiz_attempts:
            total_pct = sum(
                (att.get('score', 0) / att.get('max_score', 1) * 100)
                for att in quiz_attempts if att.get('max_score', 0) > 0
            )
            report_data['average_score'] = round(total_pct / len(quiz_attempts), 1)
        else:
            report_data['average_score'] = 0
        
        # Overall progress label
        avg = report_data['average_score']
        if avg >= 80:
            report_data['overall_progress'] = 'Excellent'
        elif avg >= 70:
            report_data['overall_progress'] = 'Good'
        elif avg >= 60:
            report_data['overall_progress'] = 'Satisfactory'
        else:
            report_data['overall_progress'] = 'Needs Improvement'
        
        # Format each quiz
        for att in quiz_attempts:
            score = att.get('score', 0)
            max_score = att.get('max_score', 1)
            pct = round((score / max_score) * 100, 1) if max_score > 0 else 0
            q = {
                'title': att.get('quiz_title', 'Unnamed Quiz'),
                'date': datetime.datetime.fromisoformat(att.get('completed_at', '1970-01-01')).strftime('%B %d, %Y')
                        if att.get('completed_at') else 'Incomplete',
                'score': score,
                'max_score': max_score,
                'score_percentage': pct,
                'topics': 'General Knowledge',
                'questions': questions_data.get(att.get('id'), []) if questions_data else []
            }
            report_data['quiz_results'].append(q)
        
        # Sort by date, desc
        report_data['quiz_results'].sort(
            key=lambda x: datetime.datetime.fromisoformat(x['date']) if x['date'] != 'Incomplete' else datetime.datetime.min,
            reverse=True
        )
        
        # Identify improvement areas
        low_topics = {q['topics'] for q in report_data['quiz_results'] if q['score_percentage'] < 70}
        for t in low_topics:
            report_data['improvement_areas'].append(f"Focus on improving understanding of {t} concepts.")
        if report_data['average_score'] < 60:
            report_data['improvement_areas'].append("Consider reviewing basic concepts across all topics.")
        if not report_data['improvement_areas']:
            report_data['improvement_areas'].append("Continue practicing to maintain your excellent progress.")
        
        # Trend analysis
        if len(quiz_attempts) >= 2:
            sorted_atts = sorted(
                quiz_attempts,
                key=lambda x: datetime.datetime.fromisoformat(x.get('completed_at', '1970-01-01'))
            )
            mid = len(sorted_atts) // 2
            first, second = sorted_atts[:mid], sorted_atts[mid:]
            fh_avg = sum((a['score']/a['max_score']*100) for a in first)/len(first)
            sh_avg = sum((a['score']/a['max_score']*100) for a in second)/len(second)
            if sh_avg > fh_avg + 5:
                report_data['trend_description'] = 'improved significantly'
            elif sh_avg > fh_avg:
                report_data['trend_description'] = 'shown improvement'
            elif sh_avg < fh_avg - 5:
                report_data['trend_description'] = 'declined'
            else:
                report_data['trend_description'] = 'remained consistent'
        else:
            report_data['trend_description'] = 'not shown a clear trend yet due to limited data'
        
        return report_data
    
    def email_report(self, report_path: str, recipient_email: str, subject: str = None) -> Dict:
        """
        Email a progress report (placeholder implementation).
        """
        if not subject:
            subject = f"AI Tutor Progress Report - {datetime.datetime.now().strftime('%B %d, %Y')}"
        return {
            'success': True,
            'recipient': recipient_email,
            'subject': subject,
            'report_path': report_path,
            'sent_at': datetime.datetime.now().isoformat(),
            'message': f"Email would be sent to {recipient_email} with report {report_path}"
        }

# Default HTML template constant
DEFAULT_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        /* ... same styles as before ... */
    </style>
</head>
<body>
    <!-- ... same template body as before ... -->
</body>
</html>'''

# Top-level helper for broader app imports

def build_report(user_data: Dict[str, Any], quiz_attempts: List[Dict[str, Any]],
                 questions_data: Optional[Dict[int, List[Dict[str, Any]]]] = None,
                 report_format: str = 'pdf') -> str:
    """
    Helper function to prepare data and generate a report.
    """
    gen = ReportGenerator()
    data = gen.prepare_report_data(user_data, quiz_attempts, questions_data)
    if report_format.lower() == 'html':
        return gen.generate_html_report(data)
    return gen.generate_pdf_report(data)
