import { Component, OnInit } from '@angular/core';

import { Breeding } from './breeding';
import { BreedingService } from './breeding.service';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'breeding.component.html',
  styleUrls: [ 'breeding.component.css' ]
})

export class AppComponent implements OnInit {
  breedings: Breeding[];
  selectedBreedings: Breeding[];
  inputPhone: string;
  loading: string;
  scrollDown: boolean;

  constructor(private breedingService: BreedingService) {
    this.inputPhone = '';
    this.selectedBreedings = [];
  }

  getBreedings(): void {
    this.loading = 'Loading';

    this.breedingService
      .getBreedings()
      .then(breedings => {
        this.loading = '';
        this.breedings = breedings
      });
  }

  search(phone: string): void {
    this.loading = 'Loading';

    this.breedingService.search(phone)
      .then(breedings => {
        this.breedings = breedings
        this.loading = ''
      });
  }

  update(state: string): void {

    let selectedBreedings = { breeding_source_list: []};

    selectedBreedings.breeding_source_list = this.breedings
      .filter(b => b.selected)
      .map(b => {
        return {
          "source_uuid": b.source_uuid,
          "qualified_status": state
        }
      });

    this.breedingService
     .update(selectedBreedings)
     .then(() => {
       this.breedings = this.breedings.filter(b => !b.selected)
       if (this.breedings.length === 0) {
         this.getBreedings();
       }

       this.loading = '更新成功';
       setTimeout(() => this.loading = '', 2000)
     });
  }

  onSelect(breeding: Breeding): void {
    breeding.selected = breeding.selected ? false: true;
  }

  onScroll(event) {
    this.scrollDown = window.scrollY > 20 ? true : false
  }

  ngOnInit(): void {
    this.getBreedings();
  }
}
