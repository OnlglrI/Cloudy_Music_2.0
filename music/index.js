const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Music service is running');
});

app.listen(port, () => {
  console.log(`Auth service listening on port ${port}`);
});
