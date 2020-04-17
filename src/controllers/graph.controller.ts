import {inject} from '@loopback/context';
import {get} from '@loopback/rest';
import {PythonService, PYTHON_SERVICE} from '../services';

export class GraphController {
  constructor(@inject(PYTHON_SERVICE) private pythonService: PythonService) {}

  @get('graph/LSTM/analyze')
  async LSTManalyze() {
    await this.pythonService.generateAnalizeGrapgsForLSTM();
    return true;
  }
}
