const http = require('http');

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

console.log(`Checking connection to: ${API_URL}`);

http.get(API_URL, (res) => {
  const { statusCode } = res;
  const contentType = res.headers['content-type'];

  let error;
  if (statusCode !== 200) {
    error = new Error('Request Failed.\n' +
                      `Status Code: ${statusCode}`);
  } else if (!/^application\/json/.test(contentType)) {
    error = new Error('Invalid content-type.\n' +
                      `Expected application/json but received ${contentType}`);
  }
  
  if (error) {
    console.error(error.message);
    res.resume();
    process.exit(1);
  }

  res.setEncoding('utf8');
  let rawData = '';
  res.on('data', (chunk) => { rawData += chunk; });
  res.on('end', () => {
    try {
      const parsedData = JSON.parse(rawData);
      console.log('Connection successful!');
      console.log('Response:', parsedData);
      process.exit(0);
    } catch (e) {
      console.error(e.message);
      process.exit(1);
    }
  });
}).on('error', (e) => {
  console.error(`Got error: ${e.message}`);
  process.exit(1);
});
