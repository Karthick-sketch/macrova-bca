import { Component, OnInit } from '@angular/core';
import { WeightTrackComponent } from './weight-track/weight-track.component';
import { DietPlanService } from '../diet-planner/diet-plan-service';
import { MetricsModel } from '../diet-planner/model/metrics.model';
import { Router } from '@angular/router';
import { LimitReachPipe } from './pipe/limitreach.pipe';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
  imports: [WeightTrackComponent, LimitReachPipe],
})
export class DashboardComponent implements OnInit {
  metrics!: MetricsModel;

  constructor(
    private dietPlanService: DietPlanService,
    private router: Router,
  ) {}

  ngOnInit() {
    this.dietPlanService.isDietPlanReachedDuration().subscribe((status) => {
      if (status) {
        this.router.navigate(['/no-active-plan']);
      } else {
        this.dietPlanService.getMetrics().subscribe({
          next: (metricsModel: MetricsModel) => {
            this.metrics = metricsModel;
          },
          error: (err: any) => {
            if (err.status === 404) {
              this.router.navigate(['/no-active-plan']);
            }
          },
        });
      }
    });
  }
}
