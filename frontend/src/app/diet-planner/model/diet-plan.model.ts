import { Gender } from '../enum/gender.enum';
import { Goal } from '../enum/goal.enum';
import { Activity } from '../enum/activity.enum';
import { Plan } from '../enum/plan.enum';

export class DietPlanModel {
  id!: string;
  title!: string;
  plan!: Plan;
  age!: number;
  gender!: Gender;
  height!: number;
  weight!: number;
  goal!: Goal;
  finalGoal!: number;
  duration!: number;
  activity!: Activity;
  active!: boolean;
}
