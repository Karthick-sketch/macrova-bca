import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  ViewChild,
} from '@angular/core';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-weight-track',
  templateUrl: './weight-track.component.html',
})
export class WeightTrackComponent implements AfterViewInit {
  chart!: Chart;

  @Input() days!: string[];
  @Input() weights!: number[];

  @ViewChild('lineChart') lineChartRef!: ElementRef;

  ngAfterViewInit(): void {
    this.chart = new Chart(this.lineChartRef.nativeElement, {
      type: 'line',
      data: {
        labels: this.days,
        datasets: [
          {
            label: 'Weight',
            data: this.weights,
            fill: false,
            backgroundColor: 'transparent',
            borderColor: 'rgb(69, 145, 223)',
            tension: 0.1,
          },
        ],
      },
    });
  }
}
