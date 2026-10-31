import { Plan } from '../enum/plan.enum';

export class DietPlanHistoryDTO {
  id!: string;
  title!: string;
  plan!: Plan;
  weight!: number;
  targetWeight!: number;
  duration!: number;
  active!: boolean;
}
