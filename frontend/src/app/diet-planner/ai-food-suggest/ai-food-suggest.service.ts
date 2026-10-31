import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AIFoodSuggestModel } from './model/ai-food-suggest.model';
import { FilterDto } from './dto/filter.dto';

@Injectable({
  providedIn: 'root',
})
export class AIFoodSuggestService {
  constructor(private httpClient: HttpClient) {}

  suggestFoods(filter: FilterDto) {
    return this.httpClient.post<AIFoodSuggestModel[]>(
      '/ai-food-suggest',
      filter,
    );
  }
}
