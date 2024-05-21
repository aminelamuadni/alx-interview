#!/usr/bin/node
const request = require('request');
const movieId = process.argv[2];

const apiUrl = `https://swapi-api.alx-tools.com/api/films/${movieId}/`;

request(apiUrl, (error, response, body) => {
    if (error) {
      console.error('Error:', error);
      return;
    }

    const filmData = JSON.parse(body);
    const characterUrls = filmData.characters;

    // Process each character URL
    characterUrls.forEach((characterUrl) => {
      request(characterUrl, (error, response, body) => {
        if (error) {
          console.error('Error:', error);
          return;
        }

        const characterData = JSON.parse(body);
        console.log(characterData.name);
      });
    });
  });
