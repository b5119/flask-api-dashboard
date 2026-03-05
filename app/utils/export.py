"""Data export utilities (PDF, CSV, Excel)"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import pandas as pd
from io import BytesIO
from datetime import datetime

def export_portfolio_pdf(holdings, user):
    """Export crypto portfolio to PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph("Cryptocurrency Portfolio Report", title_style)
    elements.append(title)
    
    # User info and date
    date_style = styles['Normal']
    date_text = Paragraph(
        f"<b>Account:</b> {user.username}<br/>"
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        date_style
    )
    elements.append(date_text)
    elements.append(Spacer(1, 20))
    
    # Portfolio table
    data = [['Coin', 'Amount', 'Purchase Price', 'Current Price', 'Value', 'Profit/Loss', 'P/L %']]
    
    total_investment = 0
    total_value = 0
    
    for holding in holdings:
        investment = holding.amount * holding.purchase_price
        current_value = holding.amount * holding.current_price
        profit_loss = current_value - investment
        pl_percentage = (profit_loss / investment * 100) if investment > 0 else 0
        
        total_investment += investment
        total_value += current_value
        
        data.append([
            holding.coin_name,
            f"{holding.amount:.6f}",
            f"${holding.purchase_price:,.2f}",
            f"${holding.current_price:,.2f}",
            f"${current_value:,.2f}",
            f"${profit_loss:,.2f}",
            f"{pl_percentage:+.2f}%"
        ])
    
    # Add totals row
    total_pl = total_value - total_investment
    total_pl_pct = (total_pl / total_investment * 100) if total_investment > 0 else 0
    
    data.append([
        'TOTAL',
        '',
        '',
        '',
        f"${total_value:,.2f}",
        f"${total_pl:,.2f}",
        f"{total_pl_pct:+.2f}%"
    ])
    
    # Create table
    table = Table(data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch])
    
    # Style table
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#667eea')),
        
        # Alignment
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ]))
    
    elements.append(table)
    
    # Summary
    elements.append(Spacer(1, 30))
    summary_style = styles['Normal']
    summary = Paragraph(
        f"<b>Portfolio Summary</b><br/>"
        f"Total Investment: ${total_investment:,.2f}<br/>"
        f"Current Value: ${total_value:,.2f}<br/>"
        f"Total Profit/Loss: ${total_pl:,.2f} ({total_pl_pct:+.2f}%)",
        summary_style
    )
    elements.append(summary)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def export_portfolio_csv(holdings):
    """Export portfolio to CSV"""
    data = []
    
    for holding in holdings:
        investment = holding.amount * holding.purchase_price
        current_value = holding.amount * holding.current_price
        profit_loss = current_value - investment
        pl_percentage = (profit_loss / investment * 100) if investment > 0 else 0
        
        data.append({
            'Coin': holding.coin_name,
            'Amount': holding.amount,
            'Purchase Price': holding.purchase_price,
            'Current Price': holding.current_price,
            'Investment': investment,
            'Current Value': current_value,
            'Profit/Loss': profit_loss,
            'P/L %': pl_percentage,
            'Purchase Date': holding.created_at.strftime('%Y-%m-%d') if holding.created_at else 'N/A'
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def export_portfolio_excel(holdings):
    """Export portfolio to Excel"""
    data = []
    
    for holding in holdings:
        investment = holding.amount * holding.purchase_price
        current_value = holding.amount * holding.current_price
        profit_loss = current_value - investment
        pl_percentage = (profit_loss / investment * 100) if investment > 0 else 0
        
        data.append({
            'Coin': holding.coin_name,
            'Amount': holding.amount,
            'Purchase Price': holding.purchase_price,
            'Current Price': holding.current_price,
            'Investment': investment,
            'Current Value': current_value,
            'Profit/Loss': profit_loss,
            'P/L %': pl_percentage,
            'Purchase Date': holding.created_at.strftime('%Y-%m-%d') if holding.created_at else 'N/A'
        })
    
    df = pd.DataFrame(data)
    
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Portfolio', index=False)
    
    buffer.seek(0)
    return buffer
