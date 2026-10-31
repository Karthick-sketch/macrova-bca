import { CaloriesDTO } from '../../dto/calories.dto';
import { MacrosDTO } from '../../dto/macros.dto';

export class AIFoodSuggestModel {
  name!: string;
  calories!: CaloriesDTO;
  macronutrients!: MacrosDTO;
  description!: string;
}
