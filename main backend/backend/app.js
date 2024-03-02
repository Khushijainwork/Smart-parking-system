const users = new Map();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());
app.use(express.static('public'));

app.post('/signup', (req, res) => {
  const { name, email, password } = req.body;

  if (users.has(email)) {
    res.status(400).send({ message: 'User already exists!' });
    return;
  }

  users.set(email, { name, password });

  console.log(`Name: ${name}`);
  console.log(`Email: ${email}`);
  console.log(`Password: ${password}`);

  res.status(200).send({ message: 'User registered successfully!' });
});

app.post('/login', (req, res) => {
  const { email, password } = req.body;

  const user = users.get(email);

  if (!user) {
    res.status(400).send({ message: 'User not found!' });
    return;
  }

  if (user.password !== password) {
    res.status(400).send({ message: 'Invalid password!' });
    return;
  }

  console.log(`Logged in: ${email}`);
  res.status(200).send({ message: 'Logged in successfully!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
