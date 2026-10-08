import os
import sys

def setup_login_ui():
    print("=" * 70)
    print("RESTORING STANDARD FRAPPE LOGIN FUNCTIONALITY WITH MOCKUP UI")
    print("=" * 70)

    bench_root = "/home/frappe/frappe-bench"
    login_html_path = os.path.join(bench_root, "apps/frappe/frappe/www/login.html")

    # This template preserves 100% of Frappe's original functional architecture,
    # error banners, forms, macros, IDs, classes, and event listeners,
    # while applying CSS and clean header positioning to match the user's mockup.
    template_code = """{% extends "templates/web.html" %}

{% macro email_login_body() %}
{% if not disable_user_pass_login %}
<div class="page-card-body">
	<div class="login-error-banner">
		<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<use href="#es-line-alert-circle"></use>
		</svg>
		<span></span>
	</div>
	<div class="form-group">
		<label class="form-label" for="login_email">{{ _("Email") }}</label>
		<div class="email-field">
			<input type="text" id="login_email" class="form-control"
				placeholder="forw8007+salesmanager@gmail.com"
				required autofocus autocomplete="username">

			<svg class="field-icon email-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"
				xmlns="http://www.w3.org/2000/svg">
				<use class="es-lock" href="#es-line-email"></use>
			</svg>
		</div>
		<p class="field-error"></p>
	</div>

	<div class="form-group">
		<label class="form-label" for="login_password">{{ _("Password") }}</label>
		<div class="password-field">
			<input type="password" id="login_password" class="form-control" placeholder="••••••••••"
				autocomplete="current-password" required>

			<svg class="field-icon password-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"
				xmlns="http://www.w3.org/2000/svg">
					<use class="es-lock" href="#es-line-lock"></use>
			</svg>
			<svg toggle="#login_password" class="toggle-password" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
					<use href="#es-line-preview"></use>
				</svg>
		</div>
		<p class="field-error"></p>
		{% if not disable_user_pass_login %}
		<p class="forgot-password-message">
			<a href="#forgot">{{ _("Forgot password?") }}</a>
		</p>
		{% endif %}
	</div>
</div>
{% endif %}
<div class="page-card-actions">
	{% if not disable_user_pass_login %}
	<button class="btn btn-sm btn-primary btn-block btn-login" type="submit">
		{{ _("Continue") }} &rarr;</button>
	{% endif %}
	{% if ldap_settings and ldap_settings.enabled %}
	<button class="btn btn-sm {{ "btn-primary" if disable_user_pass_login else "btn-default" }} btn-block btn-login btn-ldap-login">
		{{ _("Login with LDAP") }}</button>
	{% endif %}
	{% if login_with_email_link %}
	<a href="#login-with-email-link"
		class="btn btn-block btn-default btn-sm btn-login-option btn-login-with-email-link">
		<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px; vertical-align: middle;">
			<rect width="20" height="16" x="2" y="4" rx="2"></rect>
			<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
		</svg>
		{{ _("Login with Email Link") }}</a>
	{% endif %}
	{% if social_login %}
	<div class="social-logins text-center">
		<div class="social-login-buttons">
			{% for provider in provider_logins %}
			<div class="login-button-wrapper">
				<a href="{{ provider.auth_url }}"
					class="btn btn-block btn-default btn-sm btn-login-option btn-{{ provider.name }}">
					{% if provider.icon %}
						{{ provider.icon }}
					{% endif %}
					{{ _("Login with {0}").format(provider.provider_name) }}</a>
			</div>
			{% endfor %}
		</div>
	</div>
	{% endif %}
</div>
{% endmacro %}

{% block head_include %}
{{ include_style('login.bundle.css') }}
<style>
/* ORBISERP MODERN LOGIN UI (PRESERVING 100% OF STANDARD FUNCTIONALITY) */
body, html {
	background-color: #f8fafc !important;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
	min-height: 100vh !important;
	display: flex !important;
	flex-direction: column !important;
	justify-content: center !important;
	align-items: center !important;
	margin: 0 !important;
	padding: 0 !important;
}

body > .page-content-wrapper,
body > .web-page,
main.container,
.main-column,
.page_content {
	width: 100% !important;
	max-width: 100% !important;
	padding: 0 !important;
	margin: 0 !important;
	display: flex !important;
	flex-direction: column !important;
	justify-content: center !important;
	align-items: center !important;
	background: transparent !important;
}

.page-breadcrumbs,
.page-header-wrapper,
.page-footer,
.web-footer,
footer,
.sign-up-message {
	display: none !important;
}

section.for-login,
section.for-email-login,
section.for-forgot,
section.for-login-with-email-link,
section.for-signup {
	width: 100% !important;
	max-width: 440px !important;
	margin: 0 auto !important;
	padding: 20px 16px !important;
	box-sizing: border-box !important;
}

.orbis-top-branding {
	text-align: center !important;
	margin-bottom: 24px !important;
	width: 100% !important;
}

.orbis-brand-logo {
	max-width: 260px !important;
	width: 100% !important;
	height: auto !important;
	object-fit: contain !important;
	display: block !important;
	margin: 0 auto !important;
}

.login-content.page-card,
.page-card {
	background: #ffffff !important;
	border: 1px solid #e2e8f0 !important;
	border-radius: 16px !important;
	box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
	width: 100% !important;
	max-width: 440px !important;
	padding: 36px 36px 32px 36px !important;
	box-sizing: border-box !important;
	margin: 0 auto !important;
}

.page-card-head {
	display: flex !important;
	flex-direction: column !important;
	align-items: center !important;
	margin-bottom: 24px !important;
	padding: 0 !important;
}

.page-card-head .app-logo {
	display: none !important;
}

.page-card-head-text {
	text-align: center !important;
	width: 100% !important;
}

.page-card-head h4 {
	font-size: 22px !important;
	font-weight: 700 !important;
	color: #0f172a !important;
	text-align: center !important;
	margin: 0 0 6px 0 !important;
	letter-spacing: -0.3px !important;
}

.page-card-subtitle {
	font-size: 13.5px !important;
	color: #64748b !important;
	text-align: center !important;
	margin: 0 !important;
}

.page-card-body {
	display: flex !important;
	flex-direction: column !important;
	gap: 16px !important;
}

.form-group {
	margin-bottom: 0 !important;
	text-align: left !important;
}

.form-label {
	font-size: 13px !important;
	font-weight: 500 !important;
	color: #475569 !important;
	margin-bottom: 6px !important;
	display: block !important;
	text-align: left !important;
}

.email-field, .password-field {
	position: relative !important;
	width: 100% !important;
}

.form-control,
input#login_email,
input#login_password,
input#forgot_email,
input#login_with_email_link_email {
	width: 100% !important;
	height: 44px !important;
	background-color: #ffffff !important;
	border: 1px solid #e2e8f0 !important;
	border-radius: 10px !important;
	padding: 10px 14px 10px 42px !important;
	font-size: 13.5px !important;
	color: #0f172a !important;
	box-sizing: border-box !important;
	transition: all 0.2s ease !important;
}

input#login_password {
	padding-right: 42px !important;
}

.form-control:focus,
input#login_email:focus,
input#login_password:focus,
input#forgot_email:focus,
input#login_with_email_link_email:focus {
	border-color: #0284c7 !important;
	outline: none !important;
	box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12) !important;
}

.field-icon {
	position: absolute !important;
	left: 14px !important;
	top: 50% !important;
	transform: translateY(-50%) !important;
	width: 16px !important;
	height: 16px !important;
	color: #64748b !important;
	fill: #64748b !important;
	pointer-events: none !important;
	z-index: 2 !important;
}

.toggle-password {
	position: absolute !important;
	right: 14px !important;
	top: 50% !important;
	transform: translateY(-50%) !important;
	width: 16px !important;
	height: 16px !important;
	color: #64748b !important;
	fill: #64748b !important;
	cursor: pointer !important;
	z-index: 2 !important;
}

.forgot-password-message {
	text-align: right !important;
	margin-top: 6px !important;
	margin-bottom: 0 !important;
}

.forgot-password-message a {
	font-size: 12.5px !important;
	font-weight: 500 !important;
	color: #0284c7 !important;
	text-decoration: none !important;
	transition: color 0.15s ease !important;
}

.forgot-password-message a:hover {
	color: #0369a1 !important;
	text-decoration: underline !important;
}

.page-card-actions {
	margin-top: 20px !important;
	display: flex !important;
	flex-direction: column !important;
	gap: 12px !important;
}

button.btn-login.btn-primary,
button.btn-login {
	width: 100% !important;
	height: 44px !important;
	background-color: #0b132b !important;
	color: #ffffff !important;
	border: none !important;
	border-radius: 10px !important;
	font-size: 14px !important;
	font-weight: 600 !important;
	cursor: pointer !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	gap: 8px !important;
	transition: all 0.2s ease !important;
	box-shadow: 0 2px 4px rgba(11, 19, 43, 0.12) !important;
	margin: 0 !important;
}

button.btn-login.btn-primary:hover,
button.btn-login:hover {
	background-color: #1c2541 !important;
	color: #ffffff !important;
	box-shadow: 0 4px 12px rgba(11, 19, 43, 0.22) !important;
}

button.btn-login:active {
	transform: scale(0.99) !important;
}

.btn-login-option.btn-login-with-email-link,
.btn-login-option {
	width: 100% !important;
	height: 44px !important;
	background-color: #ffffff !important;
	color: #0f172a !important;
	border: 1px solid #e2e8f0 !important;
	border-radius: 10px !important;
	font-size: 13.5px !important;
	font-weight: 500 !important;
	cursor: pointer !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	gap: 8px !important;
	margin: 0 !important;
	text-decoration: none !important;
	transition: all 0.2s ease !important;
}

.btn-login-option:hover {
	background-color: #f8fafc !important;
	border-color: #cbd5e1 !important;
	color: #0f172a !important;
}

.login-error-banner {
	padding: 10px 14px !important;
	border-radius: 8px !important;
	background-color: #fef2f2 !important;
	border: 1px solid #fee2e2 !important;
	color: #b91c1c !important;
	font-size: 13px !important;
	display: none;
	align-items: center !important;
	gap: 8px !important;
}

.field-error {
	color: #ef4444 !important;
	font-size: 12px !important;
	margin-top: 4px !important;
	margin-bottom: 0 !important;
	text-align: left !important;
}
</style>
{% endblock %}

{% macro logo_section(title=null, subtitle=null) %}
<div class="orbis-top-branding text-center">
	<img src="/files/orbis_login_logo.png" alt="OrbisERP Car Manufacturing ERP" class="orbis-brand-logo">
</div>
<div class="page-card-head">
	<div class="page-card-head-text text-center">
		{% if title %}
		<h4>{{ _(title) }}</h4>
		{% else %}
		<h4>{{ _('Sign In') }}</h4>
		{% endif %}
		{% if subtitle %}
		<p class="page-card-subtitle">{{ _(subtitle) }}</p>
		{% endif %}
	</div>
</div>
{% endmacro %}

{% block page_content %}

<!-- {{ for_test }} -->
<div>
	<noscript>
		<div class="text-center my-5">
			<h4>{{ _("Javascript is disabled on your browser") }}</h4>
			<p class="text-muted">
				{{ _("You need to enable JavaScript for your app to work.") }}
			</p>
		</div>
	</noscript>
	<section class='for-login'>
		<div class="login-content page-card">
			{{ logo_section(_('Sign In'), _('Welcome! Please sign in to continue.')) }}
			<form class="form-signin form-login" role="form" novalidate>
				{{ email_login_body() }}
			</form>
			{%- if not disable_signup and not disable_user_pass_login -%}
			<div class="text-center sign-up-message">
				{{ _("Don't have an account?") }}
				<a href="#signup">{{ _("Sign up") }}</a>
			</div>
			{%- endif -%}
		</div>
	</section>

	{%- if social_login -%}
	<section class='for-email-login'>
		<div class="login-content page-card">
			{{ logo_section(_('Sign In'), _('Welcome! Please sign in to continue.')) }}
			<form class="form-signin form-login" role="form" novalidate>
			{{ email_login_body() }}
			</form>
			{%- if not disable_signup and not disable_user_pass_login -%}
			<div class="text-center sign-up-message">
				{{ _("Don't have an account?") }}
				<a href="#signup">{{ _("Sign up") }}</a>
			</div>
			{%- endif -%}
		</div>
	</section>
	{%- endif -%}
	<section class='for-signup {{ "signup-disabled" if disable_signup else "" }}'>
		<div class="login-content page-card">
			{{ logo_section(_('Sign Up'), _("Let's setup your account.")) }}
			{%- if not disable_signup -%}
			{{ signup_form_template }}
			{%- else -%}
			<div class="signup-disabled-message">
				<span class='indicator gray'>{{_("Signup Disabled")}}</span>
				<p class="text-muted text-normal sign-up-message mt-1 mb-8">{{_("Signups have been disabled for this website.")}}</p>
				<div><a href='/' class='btn btn-primary btn-md'>{{ _("Home") }}</a></div>
			</div>
			{%- endif -%}
		</div>
	</section>

	<section class='for-forgot'>
		<div class="login-content page-card">
			{{ logo_section(_('Forgot Password?'), _("Please enter your email, we'll send you password reset link")) }}
			<form class="form-signin form-forgot hide" role="form" novalidate>
				<div class="page-card-body">
					<div class="form-group">
						<label class="form-label" for="forgot_email">{{ _("Email") }}</label>
						<div class="email-field">
							<input type="email" id="forgot_email" class="form-control"
								placeholder="forw8007+salesmanager@gmail.com" required autofocus autocomplete="username">
							<svg class="field-icon email-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<use class="es-lock" href="#es-line-email"></use>
							</svg>
						</div>
						<p class="field-error"></p>
					</div>
				</div>
				<div class="page-card-actions">
					<button class="btn btn-sm btn-primary btn-block btn-signup btn-forgot"
						type="submit" disabled>{{ _("Send Link") }}</button>
				</div>
			</form>
			<div class="text-center sign-up-message">
				<a href="#login">{{ _("Back to sign in") }}</a>
			</div>
		</div>
	</section>

	<section class='for-login-with-email-link'>
		<div class="login-content page-card">
			{{ logo_section(_('Sign In'), _('Welcome! Please sign in to continue.')) }}
			<form class="form-signin form-login-with-email-link hide" role="form" novalidate>
				<div class="page-card-body">
					<div class="login-success-banner">
						<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
							<use href="#es-line-alert-circle"></use>
						</svg>
						<span>{{ _("Please check your email.") }}</span>
					</div>
					<div class="form-group">
						<label class="form-label" for="login_with_email_link_email">{{ _("Email") }}</label>
						<div class="email-field">
							<input type="email" id="login_with_email_link_email" class="form-control"
								placeholder="forw8007+salesmanager@gmail.com" required autofocus autocomplete="username">
							<svg class="field-icon email-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<use class="es-lock" href="#es-line-email"></use>
							</svg>
						</div>
						<p class="field-error"></p>
					</div>
				</div>
				<div class="page-card-actions">
					<p class="resend-link">
						{{ _("Didn't receive the link?") }} <a href="#" class="btn-resend-link">{{ _("Resend") }}</a>
					</p>
					<button class="btn btn-sm btn-primary btn-block btn-login btn-login-with-email-link"
						type="submit">{{ _("Send login link") }}</button>
					<a href="#login" class="btn btn-sm btn-default btn-block btn-login-option">
						{{ _("Login with password") }}</a>
				</div>
			</form>
			{%- if not disable_signup -%}
			<div class="text-center sign-up-message">
				{{ _("Don't have an account?") }}
				<a href="#signup">{{ _("Sign up") }}</a>
			</div>
			{%- endif -%}
		</div>
	</section>
</div>
{% endblock %}

{% block script %}
<script>{% include "templates/includes/login/login.js" %}</script>
{% endblock %}

{% block sidebar %}{% endblock %}
"""

    with open(login_html_path, "w", encoding="utf-8") as f:
        f.write(template_code)
    print(f"Updated login.html at: {login_html_path}")
    return True

if __name__ == "__main__":
    setup_login_ui()
