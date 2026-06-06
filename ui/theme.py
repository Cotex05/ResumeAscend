"""Shared visual theme for the Streamlit application."""

import streamlit as st


def inject_theme() -> None:
    """Apply the global ResumeAscend visual system."""
    st.markdown(
        """
        <style>
        :root {
            --paper: #F3EFE7;
            --ink: #1E2A27;
            --brass: #B38B4D;
            --paper-deep: #E8E1D5;
            --paper-light: #FBF9F4;
            --ink-muted: rgba(30, 42, 39, 0.68);
            --ink-faint: rgba(30, 42, 39, 0.12);
            --raised-shadow:
                10px 10px 24px rgba(94, 78, 55, 0.12),
                -8px -8px 20px rgba(255, 255, 255, 0.78);
            --inset-shadow:
                inset 3px 3px 7px rgba(94, 78, 55, 0.11),
                inset -3px -3px 7px rgba(255, 255, 255, 0.82);
        }

        html, body, [class*="css"] {
            color: var(--ink);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 82% 8%, rgba(179, 139, 77, 0.08), transparent 24rem),
                var(--paper);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            right: 1rem;
        }

        .stMainBlockContainer {
            max-width: 1180px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label {
            color: var(--ink);
        }

        h1, h2, h3 {
            letter-spacing: -0.035em;
        }

        p {
            line-height: 1.7;
        }

        a {
            color: var(--brass);
        }

        [data-testid="stSidebar"] {
            background: var(--paper-deep);
            border-right: 1px solid rgba(30, 42, 39, 0.08);
            box-shadow: 8px 0 28px rgba(94, 78, 55, 0.07);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background: var(--paper);
            border: 1px dashed rgba(30, 42, 39, 0.28);
            border-radius: 18px;
            box-shadow: var(--inset-shadow);
            padding: 1rem;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span {
            color: var(--ink-muted);
        }

        .stButton > button,
        .stFormSubmitButton > button,
        [data-testid="stPopover"] > button {
            min-height: 2.9rem;
            border-radius: 12px;
            border: 1px solid rgba(30, 42, 39, 0.14);
            background: linear-gradient(145deg, var(--paper-light), var(--paper-deep));
            color: var(--ink);
            font-weight: 650;
            box-shadow:
                5px 5px 12px rgba(94, 78, 55, 0.13),
                -4px -4px 10px rgba(255, 255, 255, 0.76);
            transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        [data-testid="stPopover"] > button:hover {
            color: var(--ink);
            border-color: var(--brass);
            transform: translateY(-1px);
            box-shadow:
                7px 7px 16px rgba(94, 78, 55, 0.15),
                -5px -5px 12px rgba(255, 255, 255, 0.82);
        }

        .stButton > button:active,
        .stFormSubmitButton > button:active,
        [data-testid="stPopover"] > button:active {
            transform: translateY(1px);
            box-shadow: var(--inset-shadow);
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: var(--ink) !important;
            color: var(--paper-light) !important;
            border-color: var(--ink) !important;
            box-shadow:
                6px 6px 14px rgba(30, 42, 39, 0.22),
                -4px -4px 10px rgba(255, 255, 255, 0.5) !important;
        }

        .stButton > button[kind="primary"],
        .stButton > button[kind="primary"] *,
        .stFormSubmitButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] * {
            color: var(--paper-light) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            color: var(--paper-light) !important;
            border-color: var(--brass) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[kind="primary"]:hover *,
        .stFormSubmitButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover * {
            color: var(--paper-light) !important;
        }

        [data-testid="stTextInput"] input {
            min-height: 3rem;
            background: var(--paper);
            color: var(--ink);
            border: 1px solid transparent;
            border-radius: 12px;
            box-shadow: var(--inset-shadow);
        }

        [data-testid="stTextInput"] input:focus {
            border-color: var(--brass);
            box-shadow: var(--inset-shadow), 0 0 0 2px rgba(179, 139, 77, 0.12);
        }

        [data-testid="stExpander"] {
            overflow: hidden;
            background: rgba(251, 249, 244, 0.66);
            border: 1px solid rgba(30, 42, 39, 0.09);
            border-radius: 16px;
            box-shadow: 5px 5px 14px rgba(94, 78, 55, 0.08);
        }

        [data-testid="stAlert"] {
            background: rgba(251, 249, 244, 0.72);
            color: var(--ink);
            border: 1px solid rgba(179, 139, 77, 0.28);
            border-radius: 14px;
            box-shadow: var(--inset-shadow);
        }

        [data-testid="stPlotlyChart"] {
            overflow: hidden;
            background: rgba(251, 249, 244, 0.62);
            border: 1px solid rgba(30, 42, 39, 0.08);
            border-radius: 20px;
            box-shadow: var(--raised-shadow);
            padding: 0.4rem;
        }

        [data-testid="stChatMessage"] {
            background: var(--paper-light);
            border: 1px solid rgba(30, 42, 39, 0.08);
            border-radius: 16px;
            box-shadow: 3px 3px 10px rgba(94, 78, 55, 0.08);
        }

        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            background: var(--ink);
            color: var(--paper-light);
        }

        [data-testid="stPopoverBody"] {
            width: min(27rem, calc(100vw - 2rem));
            max-height: min(40rem, calc(100vh - 7rem));
            overflow-y: auto;
            background: var(--paper);
            border: 1px solid rgba(30, 42, 39, 0.1);
            border-radius: 20px;
            box-shadow: 14px 14px 34px rgba(30, 42, 39, 0.18);
        }

        .resume-shell {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 2.4rem;
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .brand-seal {
            display: grid;
            width: 2.5rem;
            height: 2.5rem;
            place-items: center;
            border-radius: 50%;
            background: var(--ink);
            color: var(--paper-light);
            font-family: Georgia, serif;
            font-size: 1.15rem;
            box-shadow:
                4px 4px 10px rgba(30, 42, 39, 0.2),
                inset 0 0 0 2px rgba(179, 139, 77, 0.6);
        }

        .brand-name {
            font-size: 1.08rem;
            font-weight: 750;
            letter-spacing: -0.02em;
        }

        .brand-note {
            color: var(--ink-muted);
            font-size: 0.78rem;
        }

        .shell-status {
            color: var(--ink-muted);
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .eyebrow {
            margin-bottom: 0.75rem;
            color: var(--brass);
            font-size: 0.74rem;
            font-weight: 760;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .hero-panel,
        .paper-card,
        .metric-card,
        .profile-card,
        .quote-card,
        .detail-card {
            background: linear-gradient(145deg, rgba(251, 249, 244, 0.88), rgba(232, 225, 213, 0.68));
            border: 1px solid rgba(30, 42, 39, 0.08);
            box-shadow: var(--raised-shadow);
        }

        .hero-panel {
            position: relative;
            overflow: hidden;
            padding: clamp(2rem, 5vw, 4.6rem);
            border-radius: 28px;
        }

        .hero-panel::after {
            content: "RA";
            position: absolute;
            right: 2rem;
            bottom: -3.5rem;
            color: rgba(179, 139, 77, 0.09);
            font-family: Georgia, serif;
            font-size: clamp(8rem, 18vw, 15rem);
            line-height: 1;
        }

        .hero-panel h1 {
            position: relative;
            z-index: 1;
            max-width: 780px;
            margin: 0;
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(2.5rem, 6vw, 5.3rem);
            font-weight: 500;
            line-height: 0.98;
            letter-spacing: -0.055em;
        }

        .hero-panel p {
            position: relative;
            z-index: 1;
            max-width: 610px;
            margin: 1.4rem 0 0;
            color: var(--ink-muted);
            font-size: 1.04rem;
        }

        .feature-grid,
        .metric-grid,
        .profile-grid,
        .strength-grid {
            display: grid;
            gap: 1rem;
        }

        .feature-grid {
            grid-template-columns: repeat(3, 1fr);
            margin-top: 1.4rem;
        }

        .paper-card,
        .detail-card {
            padding: 1.35rem;
            border-radius: 18px;
        }

        .paper-card h3,
        .detail-card h3 {
            margin: 0 0 0.45rem;
            font-size: 1rem;
            letter-spacing: -0.02em;
        }

        .paper-card p,
        .detail-card p {
            margin: 0;
            color: var(--ink-muted);
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .card-index {
            display: inline-block;
            margin-bottom: 1.1rem;
            color: var(--brass);
            font-family: Georgia, serif;
            font-size: 1.3rem;
        }

        .section-heading {
            margin: 3.5rem 0 1.25rem;
        }

        .section-heading h2 {
            margin: 0;
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(1.8rem, 3vw, 2.7rem);
            font-weight: 500;
        }

        .section-heading p {
            max-width: 650px;
            margin: 0.55rem 0 0;
            color: var(--ink-muted);
        }

        .results-hero {
            padding: 2.2rem 0 1rem;
        }

        .results-hero h1 {
            max-width: 800px;
            margin: 0;
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(2.3rem, 5vw, 4.3rem);
            font-weight: 500;
            line-height: 1.02;
        }

        .results-hero p {
            color: var(--ink-muted);
        }

        .metric-grid {
            grid-template-columns: repeat(4, 1fr);
            margin: 1.5rem 0 2rem;
        }

        .metric-card {
            padding: 1.25rem;
            border-radius: 17px;
        }

        .metric-label {
            color: var(--ink-muted);
            font-size: 0.74rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .metric-value {
            margin-top: 0.35rem;
            font-family: Georgia, serif;
            font-size: 2.1rem;
            line-height: 1;
        }

        .metric-detail {
            margin-top: 0.5rem;
            color: var(--ink-muted);
            font-size: 0.78rem;
        }

        .profile-card {
            padding: 1.6rem;
            border-radius: 20px;
        }

        .profile-name {
            margin: 0;
            font-family: Georgia, serif;
            font-size: 1.7rem;
            font-weight: 500;
        }

        .profile-role {
            margin: 0.25rem 0 1.2rem;
            color: var(--brass);
            font-size: 0.88rem;
        }

        .profile-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .profile-item span {
            display: block;
            color: var(--ink-muted);
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .profile-item strong {
            display: block;
            margin-top: 0.2rem;
            font-size: 0.88rem;
            font-weight: 600;
            overflow-wrap: anywhere;
        }

        .quote-card {
            padding: clamp(1.6rem, 4vw, 2.8rem);
            border-radius: 22px;
            border-left: 4px solid var(--brass);
        }

        .quote-card p {
            margin: 0;
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(1.15rem, 2.3vw, 1.6rem);
            line-height: 1.55;
        }

        .recommendation-meta {
            color: var(--brass);
            font-size: 0.7rem;
            font-weight: 750;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .recommendation-copy {
            margin-top: 0.8rem;
            padding: 1rem;
            background: rgba(243, 239, 231, 0.72);
            border-radius: 12px;
            box-shadow: var(--inset-shadow);
        }

        .strength-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .strength-item {
            padding: 1.1rem 1.2rem;
            background: rgba(251, 249, 244, 0.68);
            border: 1px solid rgba(30, 42, 39, 0.08);
            border-radius: 15px;
            box-shadow: 4px 4px 12px rgba(94, 78, 55, 0.08);
        }

        .strength-item::before {
            content: "—";
            margin-right: 0.55rem;
            color: var(--brass);
        }

        .upload-ready {
            margin-top: 1.5rem;
            padding: 1.25rem 1.4rem;
            background: rgba(251, 249, 244, 0.7);
            border: 1px solid rgba(179, 139, 77, 0.35);
            border-radius: 16px;
            box-shadow: var(--inset-shadow);
        }

        .upload-ready strong {
            display: block;
            margin-bottom: 0.25rem;
        }

        .upload-ready span {
            color: var(--ink-muted);
            font-size: 0.84rem;
        }

        .sidebar-brand {
            padding: 0.4rem 0 1.6rem;
        }

        .sidebar-brand h2 {
            margin: 0.55rem 0 0.25rem;
            font-family: Georgia, serif;
            font-size: 1.55rem;
            font-weight: 500;
        }

        .sidebar-brand p,
        .sidebar-note {
            color: var(--ink-muted);
            font-size: 0.8rem;
        }

        .sidebar-rule {
            height: 1px;
            margin: 1.2rem 0;
            background: rgba(30, 42, 39, 0.1);
        }

        .app-footer {
            margin-top: 4rem;
            padding-top: 1.4rem;
            border-top: 1px solid rgba(30, 42, 39, 0.1);
            color: var(--ink-muted);
            font-size: 0.78rem;
            text-align: center;
        }

        .st-key-resume_chat_widget {
            position: fixed;
            right: 1.5rem;
            bottom: 1.5rem;
            width: 11.5rem;
            z-index: 999;
        }

        .st-key-resume_chat_widget button {
            border-radius: 999px;
            border-color: var(--brass);
        }

        @media (max-width: 800px) {
            .feature-grid,
            .metric-grid,
            .strength-grid {
                grid-template-columns: 1fr 1fr;
            }

            .hero-panel::after {
                opacity: 0.5;
            }
        }

        @media (max-width: 640px) {
            .stMainBlockContainer {
                padding-top: 1.2rem;
            }

            .resume-shell {
                align-items: flex-start;
            }

            .shell-status {
                display: none;
            }

            .feature-grid,
            .metric-grid,
            .strength-grid,
            .profile-grid {
                grid-template-columns: 1fr;
            }

            .hero-panel {
                padding: 2rem 1.35rem 2.4rem;
                border-radius: 22px;
            }

            .st-key-resume_chat_widget {
                right: 1rem;
                bottom: 1rem;
                width: 10.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
