import { Injectable }    from '@angular/core';
import { Headers, Response, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Breeding } from './breeding';

@Injectable()
export class BreedingService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private getBreedingUrl = '/breeding_source/admin/';
  private updateUrl = '/breeding_source/admin/';

  constructor(private http: Http) { }

  getBreedings(): Promise<Breeding[]> {
    return this.http
               .get(this.getBreedingUrl)
               .toPromise()
               .then(response => response.json() as Breeding[]);
  }

  search(phone: string): Promise<Breeding[]> {
    return this.http
               .get(`/breeding_source/admin/?phone=${phone}`)
               .toPromise()
               .then(response => response.json() as Breeding[]);
  }

  update(body: Object): Promise<void>{
      return this.http.put(this.updateUrl, JSON.stringify(body), {headers: this.headers})
                .toPromise()
                .then(() => null)
                .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}

