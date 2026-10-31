import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { DietPlanService } from '../diet-plan-service';
import { Plan } from '../enum/plan.enum';
import { DietPlanHistoryDTO } from '../dto/diet-plan-history.dto';

@Component({
  selector: 'app-no-active-diet-plan',
  templateUrl: './no-active-diet-plan.component.html',
  styleUrl: './no-active-diet-plan.component.css',
  imports: [RouterLink],
})
export class NoActiveDietPlanComponent implements OnInit {
  pastPlan: DietPlanHistoryDTO | null = null;
  Plan = Plan;

  constructor(
    private dietPlanService: DietPlanService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.dietPlanService.getPastDietPlan().subscribe((data) => {
      if (data) {
        this.pastPlan = data;
      }
    });
  }

  continuePlan(): void {
    this.router.navigate(['/diet-plan-form'], {
      state: { pastPlanId: this.pastPlan?.id },
    });
  }

  getPlan(plan: Plan) {
    return plan === Plan.WEIGHT_LOSS ? 'Weight Loss' : 'Weight Gain';
  }
}
