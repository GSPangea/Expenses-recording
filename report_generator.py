from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
from models import Expense

class ReportGenerator:
    """Generate professional PDF expense reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generate_report(self, output_path, title="Business Expense Report", preparer="", invoice_number=""):
        """
        Generate a PDF expense report.
        
        Args:
            output_path: Path where PDF should be saved
            title: Report title
            preparer: Name of person preparing report
            invoice_number: Invoice/reference number
        """
        doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=1  # Center
        )
        elements.append(Paragraph(title, title_style))
        
        # Report metadata
        report_date = datetime.now().strftime('%B %d, %Y')
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=1
        )
        
        metadata_text = f"Report Date: {report_date}"
        if preparer:
            metadata_text += f" | Prepared by: {preparer}"
        if invoice_number:
            metadata_text += f" | Invoice/Reference: {invoice_number}"
        
        elements.append(Paragraph(metadata_text, metadata_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Get all expenses and summary
        expenses = Expense.get_all()
        summary = Expense.get_summary_by_category()
        
        if not expenses:
            elements.append(Paragraph("No expenses recorded.", self.styles['Normal']))
        else:
            # Expense table by category
            elements.append(Paragraph("Expense Details", self.styles['Heading2']))
            elements.append(Spacer(1, 0.15*inch))
            
            # Group expenses by category
            expenses_by_category = {}
            for expense in expenses:
                category = expense['category']
                if category not in expenses_by_category:
                    expenses_by_category[category] = []
                expenses_by_category[category].append(expense)
            
            # Create table data with categories
            table_data = [['Date', 'Vendor', 'Category', 'Description', 'Amount']]
            total_amount = 0
            
            for category in sorted(expenses_by_category.keys()):
                # Add category header row
                table_data.append([f"** {category} **", '', '', '', ''])
                
                # Add expenses for this category
                for expense in sorted(expenses_by_category[category], key=lambda x: x['date']):
                    amount = expense['amount']
                    total_amount += amount
                    table_data.append([
                        expense['date'],
                        expense['vendor'][:20],  # Truncate long vendor names
                        '',  # Don't repeat category
                        expense['description'][:20] if expense['description'] else '',
                        f"${amount:.2f}"
                    ])
                
                # Add category subtotal
                category_total = sum(e['amount'] for e in expenses_by_category[category])
                table_data.append(['', '', '', f"Subtotal:", f"${category_total:.2f}"])
                table_data.append(['', '', '', '', ''])  # Blank row for spacing
            
            # Add total row
            table_data.append(['', '', '', 'TOTAL:', f"${total_amount:.2f}"])
            
            # Create table
            table = Table(table_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1.2*inch, 1*inch])
            
            # Style table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 11),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Summary by category
            elements.append(Paragraph("Summary by Category", self.styles['Heading2']))
            elements.append(Spacer(1, 0.15*inch))
            
            summary_data = [['Category', 'Count', 'Total']]
            for cat, total, count in summary:
                summary_data.append([cat, str(count), f"${total:.2f}"])
            
            summary_table = Table(summary_data, colWidths=[3*inch, 1*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(summary_table)
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer_text = "This expense report was generated by Expense Recorder. Please keep receipt images for verification."
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=self.styles['Normal'], fontSize=8, textColor=colors.grey)))
        
        # Build PDF
        doc.build(elements)
        
        return output_path
