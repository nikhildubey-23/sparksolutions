# TODO: Fix Email Sending on Deployed System (Vercel)

## Issue Summary
- Email sending works on local system but fails on Vercel deployment.
- Vercel blocks SMTP connections (port 587), causing Gmail SMTP to fail.
- Logs show 302 error (redirect after email failure).

## Alternative Solutions (Since SendGrid not wanted)
- [x] Try using Gmail SMTP with different port (465 SSL) instead of 587 TLS.
- [ ] Check if Vercel allows outbound connections to smtp.gmail.com.
- [ ] Consider using a different email provider that works with Vercel.
- [ ] Test with a simple curl command to check SMTP connectivity from Vercel.
- [ ] Deploy changes to Vercel and test.
