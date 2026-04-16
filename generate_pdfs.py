#!/usr/bin/env python3
"""
Generate the three missing advisor resource PDFs for the NWM Advisor Portal.
Run: python3 generate_pdfs.py
Requires: pip install reportlab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)

# ── Color palette (matches site) ──
NAVY = HexColor('#0d1b35')
TEAL = HexColor('#0e6b6b')
GRAY = HexColor('#6b7280')
LIGHT_GRAY = HexColor('#f3f4f6')
WHITE = HexColor('#ffffff')
BORDER = HexColor('#e5e7eb')
RED_ACCENT = HexColor('#b91c1c')
GOLD = HexColor('#c9a84c')

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'pdfs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

FOOTER_TEXT = "Petty Ferguson Consulting  |  For educational purposes only  |  Not investment advice"


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'DocTitle', parent=styles['Title'], fontSize=20, textColor=NAVY,
        spaceAfter=6, fontName='Helvetica-Bold', alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'], fontSize=11, textColor=GRAY,
        spaceAfter=16, fontName='Helvetica-Oblique'
    ))
    styles.add(ParagraphStyle(
        'SectionHead', parent=styles['Heading2'], fontSize=13, textColor=TEAL,
        spaceBefore=18, spaceAfter=8, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'SubHead', parent=styles['Heading3'], fontSize=10, textColor=NAVY,
        spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=9, textColor=HexColor('#1a1a2e'),
        leading=13, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'BodyBold', parent=styles['Normal'], fontSize=9, textColor=HexColor('#1a1a2e'),
        leading=13, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'Small', parent=styles['Normal'], fontSize=8, textColor=GRAY,
        leading=11, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'Warning', parent=styles['Normal'], fontSize=9, textColor=RED_ACCENT,
        leading=12, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'Footer', parent=styles['Normal'], fontSize=7, textColor=GRAY,
        alignment=TA_CENTER, fontName='Helvetica'
    ))
    return styles


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(letter[0] / 2, 30, FOOTER_TEXT)
    canvas.restoreState()


def make_table(data, col_widths=None, header=True):
    """Create a styled table."""
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]
    # alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=8, spaceBefore=4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF 1: Client Crypto Readiness Assessment
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_readiness_assessment():
    path = os.path.join(OUTPUT_DIR, 'client-crypto-readiness-assessment.pdf')
    doc = SimpleDocTemplate(path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.7*inch,
                            leftMargin=0.65*inch, rightMargin=0.65*inch)
    s = get_styles()
    story = []

    story.append(Paragraph("Client Crypto Readiness Assessment", s['DocTitle']))
    story.append(Paragraph(
        "A structured tool to identify client exposure, custody gaps, security posture, and scam risk.",
        s['DocSubtitle']))
    story.append(hr())

    # Client info
    story.append(Paragraph("Client Information", s['SubHead']))
    info_data = [
        ['Client Name:', '____________________________________', 'Date:', '________________'],
        ['Advisor:', '____________________________________', '', ''],
    ]
    t = Table(info_data, colWidths=[1*inch, 2.8*inch, 0.6*inch, 2*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>Score each section using the guidelines. Total score determines readiness level.</i>",
        s['Small']))
    story.append(Spacer(1, 6))

    # Section 1
    story.append(Paragraph("Section 1: Current Crypto Holdings (10 pts)", s['SectionHead']))
    questions = [
        "1.1  Does the client currently hold any cryptocurrency?   [ ] Yes   [ ] No   [ ] Unsure",
        "1.2  If yes, which assets?   [ ] BTC   [ ] ETH   [ ] Stablecoins   [ ] Other altcoins   [ ] NFTs   [ ] Unknown",
        "1.3  Approximate allocation as % of portfolio:   [ ] &lt;1%   [ ] 1-5% (recommended)   [ ] 5-10%   [ ] 10-25%   [ ] &gt;25%",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> Appropriate 1-5%: +10  |  Slight overallocation 5-10%: +5  |  Significant &gt;10%: +0",
        s['Small']))
    story.append(Paragraph("Section 1 Score: _____ / 10", s['BodyBold']))

    # Section 2
    story.append(Paragraph("Section 2: Custody &amp; Control (20 pts)", s['SectionHead']))
    questions = [
        "2.1  Where does the client hold crypto?   [ ] Major exchange   [ ] Smaller exchange   [ ] Hardware wallet   [ ] Mobile wallet   [ ] Multiple   [ ] Don't know",
        "2.2  Understands custodial vs. non-custodial?   [ ] Yes, can explain   [ ] Somewhat   [ ] No",
        "2.3  Has successfully withdrawn crypto from an exchange?   [ ] Yes   [ ] No   [ ] Never tried",
        "2.4  Recovery phrase stored securely?   [ ] Secure offline location   [ ] Questionable (phone/email/cloud)   [ ] No / Lost   [ ] N/A",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> Understands + secure: +20  |  Custodial reputable: +15  |  Gaps: +10  |  Red flags: +0",
        s['Small']))
    story.append(Paragraph("Section 2 Score: _____ / 20", s['BodyBold']))

    # Section 3
    story.append(Paragraph("Section 3: Security Practices (20 pts)", s['SectionHead']))
    questions = [
        "3.1  MFA on crypto accounts?   [ ] Hardware key / authenticator app   [ ] SMS-based   [ ] No   [ ] Don't know",
        "3.2  Email ever compromised?   [ ] No   [ ] Yes, changed passwords   [ ] Yes, same credentials   [ ] Don't know",
        "3.3  Unique passwords for crypto accounts?   [ ] Yes, password manager   [ ] Yes, manual   [ ] No, reuses   [ ] Don't know",
        "3.4  Reviewed security setup in past 12 months?   [ ] Yes   [ ] No   [ ] Never set up properly",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> Strong: +20  |  Adequate with gaps: +15  |  Significant gaps: +10  |  Major vulnerabilities: +0",
        s['Small']))
    story.append(Paragraph("Section 3 Score: _____ / 20", s['BodyBold']))

    # Section 4
    story.append(PageBreak())
    story.append(Paragraph("Section 4: Volatility &amp; Risk Understanding (20 pts)", s['SectionHead']))
    questions = [
        "4.1  Understands 5-20% daily swings are normal?   [ ] Yes, comfortable   [ ] Somewhat   [ ] No, expects stock-like stability",
        "4.2  Investment horizon?   [ ] Long-term (5+ yr)   [ ] Medium (1-5 yr)   [ ] Short (&lt;1 yr)   [ ] Day trading",
        "4.3  Ever panic sold during a dip?   [ ] No   [ ] Yes, once   [ ] Yes, multiple times   [ ] N/A",
        "4.4  Ever bought based on celebrity/influencer/FOMO?   [ ] No   [ ] Yes, learned   [ ] Yes, still does",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> Realistic long-term: +20  |  Some emotional: +15  |  High reactivity: +10  |  Major flags: +0",
        s['Small']))
    story.append(Paragraph("Section 4 Score: _____ / 20", s['BodyBold']))

    # Section 5
    story.append(Paragraph("Section 5: Documentation &amp; Estate Planning (15 pts)", s['SectionHead']))
    questions = [
        "5.1  Record of crypto accounts and wallets?   [ ] Yes, documented   [ ] Partial   [ ] No documentation",
        "5.2  Beneficiary able to access crypto if something happened?   [ ] Yes, clear plan   [ ] Partial   [ ] No, assets would be lost",
        "5.3  Crypto mentioned in estate plan?   [ ] Yes, with instructions   [ ] Estate plan exists but omits crypto   [ ] No estate plan",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> Complete: +15  |  Partial: +10  |  None: +0",
        s['Small']))
    story.append(Paragraph("Section 5 Score: _____ / 15", s['BodyBold']))

    # Section 6
    story.append(Paragraph("Section 6: Scam Exposure (15 pts)", s['SectionHead']))
    questions = [
        "6.1  Anyone approached with 'guaranteed returns' crypto opportunity?   [ ] No   [ ] Yes, declined   [ ] Yes, considering   [ ] Yes, invested",
        "6.2  Unsolicited messages about crypto on social media / messaging?   [ ] No   [ ] Yes, ignored   [ ] Yes, engaged",
        "6.3  Verifies URLs and sender addresses before clicking?   [ ] Always   [ ] Sometimes   [ ] Rarely   [ ] Don't know how",
    ]
    for q in questions:
        story.append(Paragraph(q, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Scoring:</b> No exposure, good awareness: +15  |  Some exposure handled: +10  |  Active risk: +0",
        s['Small']))
    story.append(Paragraph("Section 6 Score: _____ / 15", s['BodyBold']))
    story.append(Spacer(1, 12))

    # Scoring Summary
    story.append(Paragraph("Scoring Summary", s['SectionHead']))
    score_data = [
        ['Section', 'Score', 'Max'],
        ['1. Current Crypto Holdings', '', '10'],
        ['2. Custody & Control', '', '20'],
        ['3. Security Practices', '', '20'],
        ['4. Volatility & Risk Understanding', '', '20'],
        ['5. Documentation & Estate Planning', '', '15'],
        ['6. Scam Exposure', '', '15'],
        ['TOTAL', '', '100'],
    ]
    t = make_table(score_data, col_widths=[3.5*inch, 1.5*inch, 1*inch])
    story.append(t)
    story.append(Spacer(1, 12))

    # Readiness levels
    story.append(Paragraph("Readiness Levels", s['SubHead']))
    level_data = [
        ['Score', 'Level', 'Interpretation'],
        ['85-100', 'Ready', 'Strong foundations. Focus on optimization and ongoing education.'],
        ['65-84', 'Developing', 'Core understanding present but gaps exist. Prioritize weaknesses.'],
        ['40-64', 'Needs Work', 'Significant gaps. Recommend pausing new investments until addressed.'],
        ['0-39', 'At Risk', 'Major vulnerabilities. Immediate intervention needed.'],
    ]
    t = make_table(level_data, col_widths=[0.8*inch, 1.2*inch, 4*inch])
    story.append(t)
    story.append(Spacer(1, 16))

    # Action items
    story.append(Paragraph("Priority Action Items", s['SectionHead']))
    story.append(Paragraph("<i>Based on this assessment, the top 3 priorities for this client are:</i>", s['Small']))
    story.append(Spacer(1, 4))
    for i in range(1, 4):
        story.append(Paragraph(f"{i}. ___________________________________________________________________________", s['Body']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Advisor Notes", s['SectionHead']))
    story.append(Paragraph("_____________________________________________________________________________", s['Body']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("_____________________________________________________________________________", s['Body']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("_____________________________________________________________________________", s['Body']))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Next Review Date: _______________", s['BodyBold']))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"  -> {path}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF 2: Scam Red Flag Reference Card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_red_flag_card():
    path = os.path.join(OUTPUT_DIR, 'scam-red-flag-reference-card.pdf')
    doc = SimpleDocTemplate(path, pagesize=letter,
                            topMargin=0.5*inch, bottomMargin=0.7*inch,
                            leftMargin=0.55*inch, rightMargin=0.55*inch)
    s = get_styles()
    story = []

    story.append(Paragraph("Crypto Scam Red Flag Reference Card", s['DocTitle']))
    story.append(Paragraph(
        "Quick reference for advisors when clients mention crypto \"opportunities\"",
        s['DocSubtitle']))
    story.append(hr())

    # Language red flags
    story.append(Paragraph("Language Red Flags", s['SectionHead']))
    lang_data = [
        ['They Say...', 'What It Means'],
        ['"Guaranteed returns"', 'No legitimate investment guarantees returns. Ever.'],
        ['"Risk-free"', 'Crypto is inherently volatile. This is a lie.'],
        ['"Limited time offer"', 'Pressure tactics. Legitimate opportunities don\'t expire in 24 hours.'],
        ['"Double your money"', 'Classic scam promise.'],
        ['"Get in before it\'s too late"', 'FOMO manipulation.'],
        ['"Only insiders know about this"', 'If it were real, they wouldn\'t be telling strangers.'],
        ['"This is the next Bitcoin"', 'There are thousands of these. Almost all fail.'],
        ['"Celebrity X endorsed this"', 'Fake endorsements are rampant. Verify independently.'],
    ]
    story.append(make_table(lang_data, col_widths=[2.2*inch, 4.8*inch]))
    story.append(Spacer(1, 6))

    # Channel red flags
    story.append(Paragraph("Channel Red Flags", s['SectionHead']))
    chan_data = [
        ['Channel', 'Risk', 'Notes'],
        ['Unsolicited DM (Telegram, WhatsApp, Discord)', 'HIGH', 'Scammers\' preferred method'],
        ['Social media comment / reply', 'HIGH', 'Impersonation is trivial'],
        ['Dating app match', 'HIGH', '"Pig butchering" romance scams'],
        ['Random email', 'HIGH', 'Phishing, fake exchanges'],
        ['"Friend" never met in person', 'HIGH', 'Social engineering'],
        ['YouTube / TikTok influencer', 'MEDIUM', 'Many are paid promoters'],
    ]
    story.append(make_table(chan_data, col_widths=[3*inch, 0.8*inch, 3.2*inch]))
    story.append(Spacer(1, 6))

    # Common scam types
    story.append(Paragraph("Common Scam Types", s['SectionHead']))
    scam_data = [
        ['Type', 'How It Works'],
        ['Pig Butchering', 'Fake romance builds trust, introduces "investment," drains funds over time'],
        ['Fake Exchange', 'Convincing website, shows fake gains, blocks withdrawals'],
        ['Impersonation', 'Pretends to be Coinbase support, a celebrity, or a known project'],
        ['Rug Pull', 'Legitimate-looking project, team disappears with funds'],
        ['Phishing', 'Fake emails or sites that capture login credentials'],
        ['Pump & Dump', 'Hype a worthless token, sell high, leave buyers holding nothing'],
    ]
    story.append(make_table(scam_data, col_widths=[1.5*inch, 5.5*inch]))
    story.append(Spacer(1, 6))

    # What scammers say
    story.append(Paragraph("What Scammers Say About Advisors", s['SectionHead']))
    story.append(Paragraph("<i>These lines are designed to isolate clients from trusted advisors:</i>", s['Small']))
    story.append(Spacer(1, 4))
    quotes = [
        '"What are their credentials?"',
        '"They know about old money -- what do they know about new money?"',
        '"They just want the fees, that\'s why they don\'t care about crypto."',
        '"Are they protecting or preventing you?"',
        '"Do they even have Telegram?"',
    ]
    for q in quotes:
        story.append(Paragraph(f"    {q}", s['Body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Your response:</b> Recognize the pattern. Your literacy is your best counter-argument.",
        s['Body']))
    story.append(Spacer(1, 8))

    # Quick checklist
    story.append(Paragraph("Quick Client Checklist", s['SectionHead']))
    story.append(Paragraph("<i>Run through these before any crypto decision:</i>", s['Small']))
    story.append(Spacer(1, 4))
    checks = [
        "Did someone approach you, or did you find them?",
        "Are you being asked to act quickly?",
        "Were you asked to move funds to a new wallet or exchange?",
        "Are returns described as \"guaranteed\" or \"risk-free\"?",
        "Is the communication happening on Telegram, WhatsApp, or Discord?",
        "Did a romantic interest introduce you to this opportunity?",
        "Are you being asked to keep this secret from family or your advisor?",
    ]
    for c in checks:
        story.append(Paragraph(f"[ ]  {c}", s['Body']))
        story.append(Spacer(1, 2))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '2+ "Yes" answers = HIGH probability of scam. Pause and investigate.',
        s['Warning']))
    story.append(Spacer(1, 10))

    # Reporting resources
    story.append(Paragraph("Reporting Resources", s['SectionHead']))
    res_data = [
        ['Agency', 'URL'],
        ['FBI IC3 (Internet Crime Complaint Center)', 'ic3.gov'],
        ['FTC (Federal Trade Commission)', 'reportfraud.ftc.gov'],
        ['SEC (Tips, Complaints, Referrals)', 'sec.gov/tcr'],
        ['State Attorney General', 'Varies by state'],
    ]
    story.append(make_table(res_data, col_widths=[3.5*inch, 3.5*inch]))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"  -> {path}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF 3: Client Crypto Documentation Template
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_documentation_template():
    path = os.path.join(OUTPUT_DIR, 'client-crypto-documentation-template.pdf')
    doc = SimpleDocTemplate(path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.7*inch,
                            leftMargin=0.65*inch, rightMargin=0.65*inch)
    s = get_styles()
    story = []

    story.append(Paragraph("Client Crypto Documentation Template", s['DocTitle']))
    story.append(Paragraph(
        "Structured documentation for client crypto holdings -- pairs with the Readiness Assessment.",
        s['DocSubtitle']))
    story.append(Paragraph(
        "CONFIDENTIAL -- Do NOT record actual private keys or recovery phrases in this document.",
        s['Warning']))
    story.append(hr())

    # Client info
    story.append(Paragraph("Client Information", s['SubHead']))
    fields = ['Client Name', 'Account / Client ID', 'Date Created', 'Last Updated', 'Primary Advisor']
    for f in fields:
        story.append(Paragraph(f"{f}: _______________________________________________", s['Body']))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 4))

    # Section 1: Exchange accounts
    story.append(Paragraph("Section 1: Exchange &amp; Custodial Accounts", s['SectionHead']))
    story.append(Paragraph("<i>List all exchanges, brokerages, or custodial services where the client holds crypto.</i>", s['Small']))
    for acct_num in range(1, 4):
        story.append(Paragraph(f"Account {acct_num}", s['SubHead']))
        acct_fields = [
            'Platform Name: ____________________________________',
            'Account Type:  [ ] Individual  [ ] Joint  [ ] IRA  [ ] Trust  [ ] Other: ________',
            'Primary Assets Held: ______________________________',
            'Approximate Value: $ ______________________________',
            '2FA Enabled?  [ ] Yes - Authenticator App  [ ] Yes - SMS  [ ] No',
            'Withdrawal Tested?  [ ] Yes, on (date): ________  [ ] No',
            'Beneficiary on File?  [ ] Yes  [ ] No  [ ] N/A',
            'Notes: ___________________________________________',
        ]
        for f in acct_fields:
            story.append(Paragraph(f, s['Body']))
            story.append(Spacer(1, 2))
        story.append(Spacer(1, 4))

    # Section 2: Self-custody wallets
    story.append(PageBreak())
    story.append(Paragraph("Section 2: Self-Custody Wallets", s['SectionHead']))
    story.append(Paragraph("<i>List hardware wallets, software wallets, or other non-custodial solutions.</i>", s['Small']))
    for w_num in range(1, 3):
        story.append(Paragraph(f"Wallet {w_num}", s['SubHead']))
        w_fields = [
            'Wallet Type:  [ ] Hardware (Ledger, Trezor, etc.)  [ ] Mobile App  [ ] Desktop  [ ] Other: ________',
            'Wallet Name / Model: ______________________________',
            'Primary Assets Held: ______________________________',
            'Approximate Value: $ ______________________________',
            'Recovery Phrase Exists?  [ ] Yes  [ ] No  [ ] Unknown',
            'Recovery Phrase Location:  [ ] Documented securely  [ ] Client knows location  [ ] Unknown',
            'Client Tested Recovery?  [ ] Yes  [ ] No',
            'Notes: ___________________________________________',
        ]
        for f in w_fields:
            story.append(Paragraph(f, s['Body']))
            story.append(Spacer(1, 2))
        story.append(Spacer(1, 4))

    # Section 3: Summary
    story.append(Paragraph("Section 3: Total Crypto Summary", s['SectionHead']))
    summary_data = [
        ['Metric', 'Value'],
        ['Total Estimated Crypto Value', '$ _______________'],
        ['% of Total Portfolio', '______ %'],
        ['Within Recommended Range (1-5%)?', '[ ] Yes   [ ] No'],
        ['Primary Custody Method', '[ ] Custodial   [ ] Self-custody   [ ] Mixed'],
    ]
    story.append(make_table(summary_data, col_widths=[3.5*inch, 3.5*inch]))
    story.append(Spacer(1, 8))

    # Section 4: Security
    story.append(Paragraph("Section 4: Security Posture", s['SectionHead']))
    sec_data = [
        ['Item', 'Status'],
        ['All accounts have MFA (authenticator app preferred)', '[ ] Yes  [ ] No  [ ] Partial'],
        ['Client uses unique passwords per account', '[ ] Yes  [ ] No  [ ] Unknown'],
        ['Client uses a password manager', '[ ] Yes  [ ] No'],
        ['Email account secured with MFA', '[ ] Yes  [ ] No'],
        ['SIM swap protection enabled (carrier PIN)', '[ ] Yes  [ ] No  [ ] Unknown'],
        ['Client aware of phishing risks', '[ ] Yes  [ ] Needs education'],
        ['Last security review date', 'Date: _______________'],
    ]
    story.append(make_table(sec_data, col_widths=[3.8*inch, 3.2*inch]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Security Gaps Identified:", s['SubHead']))
    for i in range(1, 4):
        story.append(Paragraph(f"{i}. ___________________________________________________________________________", s['Body']))
        story.append(Spacer(1, 4))

    # Section 5: Recovery
    story.append(PageBreak())
    story.append(Paragraph("Section 5: Recovery Phrase &amp; Access Documentation", s['SectionHead']))
    story.append(Paragraph(
        "CRITICAL: Do NOT record actual recovery phrases or private keys in this document or any digital system.",
        s['Warning']))
    story.append(Spacer(1, 6))
    rec_items = [
        'Recovery phrase(s) exist for all self-custody wallets:  [ ] Yes  [ ] No  [ ] N/A',
        'Stored in secure physical location:  [ ] Yes  [ ] No',
        'Location known to client:  [ ] Yes  [ ] No',
        'Documented for estate purposes:  [ ] Yes  [ ] No',
        'Client has tested wallet recovery:  [ ] Yes  [ ] No',
    ]
    for item in rec_items:
        story.append(Paragraph(item, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Storage Method (check all that apply):", s['SubHead']))
    methods = [
        '[ ] Written on paper, stored in safe / lockbox',
        '[ ] Metal backup (fireproof / waterproof)',
        '[ ] Bank safe deposit box',
        '[ ] With attorney (sealed envelope)',
        '[ ] Split across multiple locations',
        '[ ] Stored digitally (phone notes, email, cloud) -- HIGH RISK',
        '[ ] Other: _______________________',
    ]
    for m in methods:
        story.append(Paragraph(m, s['Body']))
        story.append(Spacer(1, 2))

    # Section 6: Estate
    story.append(Spacer(1, 8))
    story.append(Paragraph("Section 6: Estate Planning &amp; Beneficiary Access", s['SectionHead']))
    estate_items = [
        'Estate plan exists:  [ ] Yes  [ ] No',
        'Estate plan addresses crypto assets:  [ ] Yes  [ ] No',
        'Executor / beneficiary knows crypto exists:  [ ] Yes  [ ] No',
        'Executor / beneficiary knows where to find access info:  [ ] Yes  [ ] No',
        'Instructions for beneficiaries documented:  [ ] Yes  [ ] No',
        'Attorney aware of crypto holdings:  [ ] Yes  [ ] No  [ ] N/A',
    ]
    for item in estate_items:
        story.append(Paragraph(item, s['Body']))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Designated Contacts for Crypto Access:", s['SubHead']))
    contacts_data = [
        ['Role', 'Name', 'Relationship', 'Has Access Instructions?'],
        ['Executor', '', '', '[ ] Yes  [ ] No'],
        ['Beneficiary 1', '', '', '[ ] Yes  [ ] No'],
        ['Beneficiary 2', '', '', '[ ] Yes  [ ] No'],
        ['Attorney', '', '', '[ ] Yes  [ ] No'],
    ]
    story.append(make_table(contacts_data, col_widths=[1.2*inch, 2*inch, 1.8*inch, 2*inch]))

    # Section 7: Tax
    story.append(Paragraph("Section 7: Transaction History &amp; Tax", s['SectionHead']))
    tax_data = [
        ['Item', 'Status'],
        ['Client maintains transaction records', '[ ] Yes  [ ] Partial  [ ] No'],
        ['Client uses crypto tax software', '[ ] Yes - Name: ________  [ ] No'],
        ['CPA / tax preparer aware of crypto holdings', '[ ] Yes  [ ] No'],
        ['Cost basis documented', '[ ] Yes  [ ] Partial  [ ] No'],
    ]
    story.append(make_table(tax_data, col_widths=[3.5*inch, 3.5*inch]))

    # Section 8: Advisor notes
    story.append(PageBreak())
    story.append(Paragraph("Section 8: Advisor Notes", s['SectionHead']))
    story.append(Paragraph("Initial Assessment Notes:", s['SubHead']))
    for _ in range(4):
        story.append(Paragraph("_____________________________________________________________________________", s['Body']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Recommended Actions:", s['SubHead']))
    action_data = [
        ['Priority', 'Action Item', 'Target Date', 'Done?'],
        ['1', '', '', '[ ]'],
        ['2', '', '', '[ ]'],
        ['3', '', '', '[ ]'],
        ['4', '', '', '[ ]'],
        ['5', '', '', '[ ]'],
    ]
    story.append(make_table(action_data, col_widths=[0.8*inch, 3.5*inch, 1.5*inch, 1.2*inch]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Follow-up Schedule:", s['SubHead']))
    followup_data = [
        ['Review Type', 'Frequency', 'Next Date'],
        ['Security Review', 'Annual', ''],
        ['Allocation Check', 'Quarterly', ''],
        ['Estate Plan Review', 'Annual', ''],
        ['Full Documentation Update', 'Annual', ''],
    ]
    story.append(make_table(followup_data, col_widths=[2.5*inch, 2*inch, 2.5*inch]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Change Log:", s['SubHead']))
    log_data = [
        ['Date', 'Change Description', 'Updated By'],
        ['', '', ''],
        ['', '', ''],
        ['', '', ''],
    ]
    story.append(make_table(log_data, col_widths=[1.5*inch, 3.5*inch, 2*inch]))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"  -> {path}")


if __name__ == '__main__':
    print("Generating advisor resource PDFs...")
    generate_readiness_assessment()
    generate_red_flag_card()
    generate_documentation_template()
    print("Done! PDFs are in assets/pdfs/")
