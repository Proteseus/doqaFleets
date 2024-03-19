import os
import logging
from PyPDF2 import PdfMerger
from django.core.files import File
from django.db import models
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.conf import settings
from django.db.models import Avg, F

from .models import Employee, Vehicle, Alert, Maintenance, Trip, Inventory

# Set up logging with a custom format including timestamp
report_logs = os.path.join(settings.MEDIA_ROOT, 'reports', 'report_generation.log')
logging.basicConfig(filename=report_logs, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_fleet_overview_report():
    logging.info('Generating fleet overview report...')
    try:
        # Retrieve fleet data
        total_vehicles = Vehicle.objects.count()
        total_assigned_vehicles = Vehicle.objects.filter(driver_id__isnull=False).count()
        total_unassigned_vehicles = Vehicle.objects.filter(driver_id__isnull=True).count()
        average_fuel_level = Vehicle.objects.aggregate(avg_fuel=models.Avg('fuel'))['avg_fuel']

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'fleet_overview_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Fleet Overview Report'],
            ['Total Vehicles', total_vehicles],
            ['Assigned Vehicles', total_assigned_vehicles],
            ['Unassigned Vehicles', total_unassigned_vehicles],
            ['Average Fuel Level', f'{average_fuel_level:.2f}' if average_fuel_level else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated fleet overview report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating fleet overview report: {e}')

def generate_maintenance_summary_report():
    logging.info('Generating maintenance summary report...')
    try:
        # Aggregate maintenance data
        total_pending_tasks = Maintenance.objects.filter(status='PENDING').count()
        total_completed_tasks = Maintenance.objects.filter(status='COMPLETED').count()
        avg_completion_time = Maintenance.objects.filter(status='COMPLETED').aggregate(avg_days=models.Avg('completed_date' - 'scheduled_date'))

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'maintenance_summary_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Maintenance Summary Report'],
            ['Total Pending Tasks', total_pending_tasks],
            ['Total Completed Tasks', total_completed_tasks],
            ['Average Completion Time (Days)', f'{avg_completion_time:.2f}' if avg_completion_time else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated maintenance summary report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating maintenance summary report: {e}')

def generate_employee_utilization_report():
    logging.info('Generating employee utilization report...')
    try:
        # Analyze employee utilization
        total_employees = Employee.objects.count()
        assigned_employees = Employee.objects.filter(assigned=True).count()
        unassigned_employees = Employee.objects.filter(assigned=False).count()
        utilization_percentage = (assigned_employees / total_employees) * 100 if total_employees != 0 else 0

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'employee_utilization_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Employee Utilization Report'],
            ['Total Employees', total_employees],
            ['Assigned Employees', assigned_employees],
            ['Unassigned Employees', unassigned_employees],
            ['Utilization Percentage', f'{utilization_percentage:.2f}%' if total_employees != 0 else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated employee utilization report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating employee utilization report: {e}')


def generate_trip_performance_report():
    logging.info('Generating fleet trip performance report...')
    try:
        # Analyze trip performance
        total_trips = Trip.objects.count()
        completed_trips = Trip.objects.filter(status='COMPLETED').count()
        on_time_trips = Trip.objects.filter(status='COMPLETED', planned_end_time__lte=F('actual_end_time')).count()
        delayed_trips = Trip.objects.filter(status='COMPLETED', planned_end_time__gt=F('actual_end_time')).count()
        completion_rate = (completed_trips / total_trips) * 100 if total_trips != 0 else 0

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'trip_performance_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Trip Performance Report'],
            ['Total Trips', total_trips],
            ['Completed Trips', completed_trips],
            ['On-Time Trips', on_time_trips],
            ['Delayed Trips', delayed_trips],
            ['Completion Rate', f'{completion_rate:.2f}%' if total_trips != 0 else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated fleet trip performance report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating trip performance report: {e}')

def generate_employee_vehicle_relationships_report():
    logging.info('Generating employee vehicle relationships report...')
    try:
        # Analyze employee and vehicle relationships
        total_vehicles = Vehicle.objects.count()
        vehicles_with_driver = Vehicle.objects.exclude(driver_id__isnull=True).count()
        vehicles_without_driver = total_vehicles - vehicles_with_driver
        vehicles_per_driver = vehicles_with_driver / total_vehicles if total_vehicles != 0 else 0

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'employee_vehicle_relationships_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Employee and Vehicle Relationships Report'],
            ['Total Vehicles', total_vehicles],
            ['Vehicles with Driver', vehicles_with_driver],
            ['Vehicles without Driver', vehicles_without_driver],
            ['Average Vehicles per Driver', f'{vehicles_per_driver:.2f}' if total_vehicles != 0 else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated employee vehicle relationships report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating employee vehicle relationships report: {e}')

def generate_system_health_report():
    logging.info('Generating system health report...')
    try:
        # Analyze overall system health
        total_vehicles = Vehicle.objects.count()
        active_vehicles = Vehicle.objects.filter(driver_id__isnull=False).count()
        inactive_vehicles = total_vehicles - active_vehicles
        average_vehicle_age = Vehicle.objects.aggregate(avg_age=models.Avg('year'))['avg_age']

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'system_health_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Overall System Health Report'],
            ['Total Vehicles', total_vehicles],
            ['Active Vehicles', active_vehicles],
            ['Inactive Vehicles', inactive_vehicles],
            ['Average Vehicle Age', f'{average_vehicle_age:.2f}' if average_vehicle_age else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated system health report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating system health report: {e}')

def generate_fuel_efficiency_report():
    logging.info('Generating fuel efficiency report...')
    try:
        # Analyze fuel efficiency
        total_vehicles = Vehicle.objects.count()
        vehicles_with_fuel_data = Vehicle.objects.exclude(fuel__isnull=True).count()
        avg_fuel_level = Vehicle.objects.aggregate(avg_fuel=models.Avg('fuel'))['avg_fuel']

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'fuel_efficiency_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Fuel Efficiency Report'],
            ['Total Vehicles', total_vehicles],
            ['Vehicles with Fuel Data', vehicles_with_fuel_data],
            ['Average Fuel Level', f'{avg_fuel_level:.2f}' if avg_fuel_level else 'N/A']
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated fuel efficiency report.')    
        return filename
    except Exception as e:
        logging.error(f'Error generating fuel efficiency report: {e}')

def generate_vehicle_maintenance_status_report():
    logging.info('Generating vehicle maintenance status report...')
    try:
        # Analyze vehicle maintenance status
        total_vehicles = Vehicle.objects.count()
        vehicles_with_pending_maintenance = Vehicle.objects.filter(maintenance__status='PENDING').distinct().count()
        vehicles_with_completed_maintenance = Vehicle.objects.filter(maintenance__status='COMPLETED').distinct().count()
        vehicles_without_maintenance = total_vehicles - vehicles_with_pending_maintenance - vehicles_with_completed_maintenance

        # Create PDF report
        filename = os.path.join(settings.MEDIA_ROOT, 'reports', 'vehicle_maintenance_status_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        data = [
            ['Vehicle Maintenance Status Report'],
            ['Total Vehicles', total_vehicles],
            ['Vehicles with Pending Maintenance', vehicles_with_pending_maintenance],
            ['Vehicles with Completed Maintenance', vehicles_with_completed_maintenance],
            ['Vehicles without Maintenance', vehicles_without_maintenance]
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        # Save PDF report
        doc.build(elements)
        logging.info('Generated vehicle maintenance status report.')
        return filename
    except Exception as e:
        logging.error(f'Error generating vehicle maintenance status report: {e}')

def generate_and_merge_reports():
    logging.info('Generating summary report...')
    try:
        # Generate individual reports
        reports = [
            generate_fleet_overview_report(),
            generate_employee_utilization_report(),
            generate_trip_performance_report(),
            generate_employee_vehicle_relationships_report(),
            generate_system_health_report(),
            generate_fuel_efficiency_report(),
            generate_vehicle_maintenance_status_report()
        ]

        # Merge individual reports into one PDF file
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', 'all_reports.pdf')
        merger = PdfMerger()

        for report in reports:
            merger.append(report)

        # Save the merged PDF file
        with open(output_pdf_path, 'wb') as output_pdf:
            merger.write(output_pdf)
            
        logging.info('Generated summary report.')
        return output_pdf_path
    except Exception as e:
        logging.error(f'Error generating summary report: {e}')


