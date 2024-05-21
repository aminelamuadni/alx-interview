#!/usr/bin/node
const request = require('request');
const apiUrl = 'https://swapi-api.alx-tools.com/api';

if (process.argv.length > 2) {
  request(`${apiUrl}/films/${process.argv[2]}/`, (err, response, body) => {
    if (err) {
      console.error(err);
      return;
    }
    const characterUrls = JSON.parse(body).characters;
    const characterPromises = characterUrls.map(url => new Promise((resolve, reject) => {
      request(url, (error, res, body) => {
        if (error) {
          reject(error);
        } else {
          resolve(JSON.parse(body).name);
        }
      });
    }));

    Promise.all(characterPromises)
      .then(names => console.log(names.join('\n')))
      .catch(error => console.error(error));
  });
}
