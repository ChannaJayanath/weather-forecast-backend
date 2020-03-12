import {bind, BindingKey, /* inject, */ BindingScope} from '@loopback/core';
import * as path from 'path';
import {PythonShell} from 'python-shell';
import {promisify} from 'util';

const pyRunAsync = promisify(PythonShell.run);

@bind({scope: BindingScope.TRANSIENT})
export class PythonService {
  constructor(/* Add @inject to inject parameters */) {}

  /*
   * Add service methods here
   */
  async genarateGraph() {
    let days_to_forecast_RF = {
      Batalagoda_RF: 20,
      Kurunegala_RF: 30,
      Maspotha_RF: 40,
    };
    let current_states_RF = {
      Batalagoda_RF: 'NoRain',
      Kurunegala_RF: 'NoRain',
      Maspotha_RF: 'NoRain',
    };
    let days_to_forecast_FS = 42;
    let current_FS = 'Critical';

    var RunOptions: Options = {
      mode: 'text',
      args: [
        JSON.stringify(days_to_forecast_RF),
        JSON.stringify(current_states_RF),
        days_to_forecast_FS,
        current_FS,
      ],
    };
    try {
      let result: any = await pyRunAsync(
        path.join(__dirname, '../../src/python/scripts/predict-status.py'),
        <Options>RunOptions,
      );
      console.log(JSON.stringify(result));
      return <string[]>result;
    } catch (e) {
      console.log(e);
    } finally {
      console.log('We finished here python service');
    }
  }
}
export const PYTHON_SERVICE = BindingKey.create<PythonService>(
  'service.pythonService',
);

export interface Options {
  mode?: 'text' | 'json' | 'binary';
  formatter?: (param: string) => any;
  parser?: (param: string) => any;
  stderrParser?: (param: string) => any;
  encoding?: string;
  pythonPath?: string;
  /**
   * see https://docs.python.org/3.7/using/cmdline.html
   */
  pythonOptions?: string[];
  /**
   * overrides scriptPath passed into PythonShell constructor
   */
  scriptPath?: string;
  /**
   * arguments to your program
   */
  args?: any[];
}
