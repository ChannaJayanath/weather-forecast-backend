import {inject} from '@loopback/context';
import {post, requestBody} from '@loopback/rest';
import {PythonService, PYTHON_SERVICE} from '../services';

export class MarkovController {
  constructor(@inject(PYTHON_SERVICE) private pythonService: PythonService) {}

  @post('markov/getStates')
  async markovGetStatus(@requestBody() req: getStatesReq) {
    console.log(req);
    return await this.pythonService.markovGetStatus(req);
  }
}

export interface getStatesReq {
  daysToForecast: number;
  currentRainBatalagoda: string;
  currentRainKurunegala: string;
  currentRainMaspota: string;
  currentFloodState: string;
}
