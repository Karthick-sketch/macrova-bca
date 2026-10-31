import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DietPlanOverviewModel } from '../model/diet-plan-overview.model';
import { DietPlanService } from '../diet-plan-service';

@Component({
  selector: 'app-diet-plan-overview',
  templateUrl: 'diet-plan-overview.component.html',
  styleUrl: 'diet-plan-overview.component.css',
  imports: [DatePipe, RouterLink],
})
export class DietPlanOverviewComponent implements OnInit {
  plans!: DietPlanOverviewModel[];

  constructor(
    private route: ActivatedRoute,
    private dietPlanService: DietPlanService,
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.dietPlanService.getDietPlanOverview(id).subscribe((plans) => {
        this.plans = plans;
      });
    }
  }
}
