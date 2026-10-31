import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe, NgTemplateOutlet } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DietPlanService } from '../diet-plan-service';
import { DietPlanTrackModel } from '../model/diet-plan-track.model';
import { MealKcalDTO } from '../dto/meal-kcal.dto';

@Component({
  selector: 'app-diet-plan',
  templateUrl: './diet-plan-track-overview.component.html',
  styleUrl: './diet-plan-track-overview.component.css',
  imports: [NgTemplateOutlet, FormsModule, DatePipe],
})
export class DietPlanTrackOverviewComponent implements OnInit {
  dietPlanTrack!: DietPlanTrackModel;
  meals!: MealKcalDTO;
  kcalPercentage!: number;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private dietPlanService: DietPlanService,
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.dietPlanService.getDietPlanTrackById(id).subscribe({
        next: (dietPlanTrackModel: DietPlanTrackModel) => {
          this.dietPlanTrack = dietPlanTrackModel;
          this.meals = dietPlanTrackModel.mealKcal;
          this.setKcalPercentage();
        },
        error: (err) => {
          if (err.status === 404) {
            this.router.navigate(['/not-found']);
          }
        },
      });
    }
  }

  setKcalPercentage() {
    this.kcalPercentage =
      (this.dietPlanTrack.intake.taken / this.dietPlanTrack.intake.total) * 100;
  }
}
