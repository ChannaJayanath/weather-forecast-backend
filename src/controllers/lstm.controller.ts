import {inject} from '@loopback/context';
import {get, RestBindings} from '@loopback/rest';
import {PythonService, PYTHON_SERVICE} from '../services';

export class LstmController {
  constructor(
    @inject(PYTHON_SERVICE) private pythonService: PythonService,
    @inject(RestBindings.Http.RESPONSE) private response: any,
  ) {
    (this.response as any).setTimeout(3600000);
  }

  @get('LSTM/model/train')
  async modelTrainLSTM() {
    return await this.pythonService.trainModelLSTM();
  }

  @get('LSTM/model/test')
  async modelTestLSTM() {
    return await this.pythonService.testModelLSTM();
  }
}
