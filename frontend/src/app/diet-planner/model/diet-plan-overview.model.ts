import { CaloriesDTO } from '../dto/calories.dto';

export class DietPlanOverviewModel {
  id!: string;
  weight!: number;
  tdee!: number;
  intake!: CaloriesDTO;
  protein!: CaloriesDTO;
  carbs!: CaloriesDTO;
  fat!: CaloriesDTO;
  createdAt!: Date;
}
