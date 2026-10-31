import { CaloriesDTO } from '../dto/calories.dto';
import { MealKcalDTO } from '../dto/meal-kcal.dto';

export class DietPlanTrackModel {
  id!: string;
  weight!: number;
  tdee!: number;
  intake!: CaloriesDTO;
  mealKcal!: MealKcalDTO;
  createdAt!: string;
  dayCount!: number;
  dietPlanId!: string;
}
