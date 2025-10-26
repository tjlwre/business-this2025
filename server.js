const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the frontend/static directory
app.use(express.static('frontend/static'));

// Route handlers
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/index.html'));
});

app.get('/app', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/app.html'));
});

app.get('/demo', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/index.html'));
});

app.get('/pricing', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/pricing.html'));
});

app.get('/about', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/about.html'));
});

app.get('/contact', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/contact.html'));
});

app.get('/privacy', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/privacy.html'));
});

app.get('/terms', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/terms.html'));
});

// Catch-all handler for client-side routing
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/static/index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
