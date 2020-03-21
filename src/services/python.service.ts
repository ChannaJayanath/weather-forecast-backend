import {bind, BindingKey, /* inject, */ BindingScope} from '@loopback/core';
import * as path from 'path';
import {PythonShell} from 'python-shell';
import {promisify} from 'util';
import {getStatesReq} from '../controllers';

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

  async markovGetStatus(req: getStatesReq) {
    let days_to_forecast_RF = {
      Batalagoda_RF: req.daysToForecast,
      Kurunegala_RF: req.daysToForecast,
      Maspotha_RF: req.daysToForecast,
    };
    let current_states_RF = {
      Batalagoda_RF: req.currentRainBatalagoda,
      Kurunegala_RF: req.currentRainKurunegala,
      Maspotha_RF: req.currentRainMaspota,
    };
    let days_to_forecast_FS = req.daysToForecast;
    let current_FS = req.currentFloodState;
    console.log(days_to_forecast_RF);
    console.log(current_states_RF);

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
        path.join(__dirname, '../../src/python/markov/predict-status.py'),
        <Options>RunOptions,
      );
      // console.log(JSON.parse(result));
      return JSON.parse(result[0]);
    } catch (e) {
      console.log(e);
    } finally {
      console.log('We finished here python service');
    }
  }

  async getNextFlood(req: getStatesReq) {
    let current_FS = req.currentFloodState;
    var RunOptions: Options = {
      mode: 'text',
      args: [current_FS],
    };
    try {
      let result: any = await pyRunAsync(
        path.join(__dirname, '../../src/python/markov/next-flood.py'),
        <Options>RunOptions,
      );
      // console.log(JSON.parse(result));
      return JSON.parse(result[0]);
    } catch (e) {
      console.log(e);
    } finally {
      console.log('We finished here python service');
    }
  }

  async generateAnalizeGrapgsForLSTM() {
    var RunOptions: Options = {
      mode: 'text',
      args: [],
    };
    try {
      let result: any = await pyRunAsync(
        path.join(__dirname, '../../src/python/LSTM/analyze-data.py'),
        <Options>RunOptions,
      );
      // console.log(JSON.parse(result));
      return result[0];
    } catch (e) {
      console.log(e);
    } finally {
      console.log('We finished here python service');
    }
  }

  async trainModelLSTM() {
    var RunOptions: Options = {
      mode: 'text',
      args: [],
    };
    try {
      let result: any = await pyRunAsync(
        path.join(__dirname, '../../src/python/LSTM/train-model.py'),
        <Options>RunOptions,
      );
      if (result) {
        return 'done';
      } else {
        return 'failed';
      }
    } catch (e) {
      console.log(e);
    } finally {
      console.log('We finished here python service');
    }
  }

  async testModelLSTM() {
    var RunOptions: Options = {
      mode: 'text',
      args: [],
    };
    try {
      let result: any = await pyRunAsync(
        path.join(__dirname, '../../src/python/LSTM/test-model.py'),
        <Options>RunOptions,
      );
      // console.log(JSON.parse(result));
      return JSON.parse(result[0]);
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
