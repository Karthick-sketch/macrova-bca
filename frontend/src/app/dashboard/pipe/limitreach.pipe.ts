import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'limitreach',
})
export class LimitReachPipe implements PipeTransform {
  transform(value: number, isPercent: boolean) {
    return value < 100 ? value : isPercent ? 100 : '>100';
  }
}
