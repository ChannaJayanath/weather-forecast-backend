import {inject} from '@loopback/context';
import {post, requestBody} from '@loopback/rest';
import {PythonService, PYTHON_SERVICE} from '../services';

export class GraphController {
  constructor(@inject(PYTHON_SERVICE) private pythonService: PythonService) {}

  @post('test')
  async testTest(@requestBody() req: any) {
    console.log(req);
    return await this.pythonService.genarateGraph();
  }
}
