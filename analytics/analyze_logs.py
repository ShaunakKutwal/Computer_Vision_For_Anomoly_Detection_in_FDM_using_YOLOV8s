# src/analyze_logs.py
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter

def analyze_alerts(log_file=None):
    """
    Analyze alert history from log files
    """
    print("="*50)
    print("ALERT HISTORY ANALYSIS")
    print("="*50)
    
    if log_file is None:
        # Find latest log file
        log_dir = 'alerts/logs'
        if not os.path.exists(log_dir):
            print("No alerts folder found")
            return
        
        json_files = [f for f in os.listdir(log_dir) if f.endswith('.json')]
        if not json_files:
            print("No alert logs found")
            return
        
        # Use most recent
        log_file = os.path.join(log_dir, sorted(json_files)[-1])
    
    print(f"Analyzing: {log_file}")
    
    # Load alerts
    with open(log_file, 'r') as f:
        alerts = json.load(f)
    
    if len(alerts) == 0:
        print("No alerts in this log file")
        return
    
    print(f"\nTotal alerts: {len(alerts)}")
    
    # Count by defect type
    defect_counts = Counter([a['defect'] for a in alerts])
    
    print("\nDefect breakdown:")
    for defect, count in defect_counts.most_common():
        percentage = (count / len(alerts)) * 100
        print(f"  {defect}: {count} ({percentage:.1f}%)")
    
    # Time analysis
    if len(alerts) > 1:
        try:
            times = [datetime.fromisoformat(a['timestamp']) for a in alerts]
            time_range = times[-1] - times[0]
            print(f"\nTime range: {time_range}")
            print(f"Average alerts per day: {len(alerts) / max(time_range.days, 1):.1f}")
        except:
            print("\nCould not analyze time data")
    
    # Confidence analysis
    confidences = [a['confidence'] for a in alerts]
    avg_conf = sum(confidences) / len(confidences)
    print(f"\nAverage confidence: {avg_conf:.1f}%")
    print(f"Min confidence: {min(confidences):.1f}%")
    print(f"Max confidence: {max(confidences):.1f}%")
    
    # Plot if requested
    plot = input("\nGenerate plot? (y/n): ").lower()
    if plot == 'y':
        plt.figure(figsize=(10, 6))
        
        # Defect distribution pie chart
        plt.subplot(1, 2, 1)
        plt.pie(defect_counts.values(), labels=defect_counts.keys(), autopct='%1.1f%%')
        plt.title('Defect Distribution')
        
        # Confidence histogram
        plt.subplot(1, 2, 2)
        plt.hist(confidences, bins=10, edgecolor='black')
        plt.title('Confidence Distribution')
        plt.xlabel('Confidence (%)')
        plt.ylabel('Frequency')
        
        plt.tight_layout()
        plt.show()
    
    return alerts

def export_alerts_csv(log_file, output_file='alerts_export.csv'):
    """
    Export alerts to CSV format
    """
    import csv
    
    with open(log_file, 'r') as f:
        alerts = json.load(f)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Defect', 'Confidence', 'Snapshot'])
        
        for alert in alerts:
            writer.writerow([
                alert['timestamp'],
                alert['defect'],
                alert['confidence'],
                alert.get('snapshot', 'N/A')
            ])
    
    print(f"Exported {len(alerts)} alerts to {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze alert logs')
    parser.add_argument('--log', type=str, help='Specific log file to analyze')
    parser.add_argument('--export', type=str, help='Export to CSV file')
    
    args = parser.parse_args()
    
    if args.export:
        export_alerts_csv(args.log if args.log else 'alerts/logs/alerts_latest.json', args.export)
    else:
        analyze_alerts(args.log)