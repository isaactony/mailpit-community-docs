const nodemailer = require("nodemailer");

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || "localhost",
  port: Number(process.env.SMTP_PORT || 1025),
  secure: false, // Mailpit doesn't use TLS by default
});

transporter
  .sendMail({
    from: "App <noreply@example.com>",
    to: "ada@example.com",
    subject: "Welcome to the app",
    text: "Thanks for signing up.",
    html: "<p>Thanks for signing up.</p>",
  })
  .then((info) => console.log("Sent:", info.messageId))
  .catch((err) => {
    console.error("Send failed:", err.message);
    process.exit(1);
  });
