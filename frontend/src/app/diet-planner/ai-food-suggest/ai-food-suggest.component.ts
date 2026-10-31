import { Component } from '@angular/core';
import { AIFoodSuggestModel } from './model/ai-food-suggest.model';
import { AIFoodSuggestService } from './ai-food-suggest.service';
import { FilterDto } from './dto/filter.dto';

@Component({
  selector: 'app-ai-food-suggest',
  templateUrl: './ai-food-suggest.component.html',
  styleUrl: './ai-food-suggest.component.css',
})
export class AIFoodSuggestComponent {
  filters = {
    mealFilters: ['Breakfast', 'Lunch', 'Snack', 'Dinner'],
    foodFilters: ['Vegetarian', 'Non-vegetarian', 'Low-carb'],
    cuisineFilters: ['Indian', 'Chinese', 'Japanese', 'Thai'],
  };
  selected: FilterDto = {
    mealFilter: 'Breakfast',
    foodFilter: 'Vegetarian',
    cuisineFilter: 'Indian',
  };
  isLoading = false;
  isError = false;

  aiFoodSuggests!: AIFoodSuggestModel[];

  constructor(private aiFoodSuggestService: AIFoodSuggestService) {}

  addMealFilter(filter: string) {
    this.selected.mealFilter = filter;
  }

  addFoodFilter(filter: string) {
    this.selected.foodFilter = filter;
  }

  addCuisineFilter(filter: string) {
    this.selected.cuisineFilter = filter;
  }

  suggest() {
    this.isLoading = true;
    this.isError = false;
    this.aiFoodSuggestService.suggestFoods(this.selected).subscribe({
      next: (aiFoodSuggestModel: AIFoodSuggestModel[]) => {
        this.aiFoodSuggests = aiFoodSuggestModel;
        this.isLoading = false;
      },
      error: (err) => {
        if (err.status === 410) {
          this.isLoading = false;
          this.isError = true;
        }
      },
    });
  }
}
