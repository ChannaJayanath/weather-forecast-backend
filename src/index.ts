import {WeatherForecastApplication} from './application';
import {ApplicationConfig} from '@loopback/core';

export {WeatherForecastApplication};

export async function main(options: ApplicationConfig = {}) {
  const app = new WeatherForecastApplication(options);
  await app.boot();
  await app.start();

  const url = app.restServer.url;
  console.log(`Server is running at ${url}`);
  console.log(`Try ${url}/ping`);

  return app;
}
