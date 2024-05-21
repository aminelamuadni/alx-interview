#!/usr/bin/node
const request = require('request');
const movieId = process.argv[2];

request(`https://swapi-api.alx-tools.com/api/films/${movieId}/`, { json: true }, (err, res, body) => {
  if (err) { return console.log(err); }
  let characters = body.characters;
  characters.forEach(charUrl => {
    request(charUrl, { json: true }, (err, res, body) => {
      if (err) { return console.log(err); }
      console.log(body.name);
    });
  });
});
