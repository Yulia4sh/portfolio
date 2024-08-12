#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
Description:
This script provides a simple organizer to manage events with dates and times. 
It allows users to add events to a file and retrieve them based on specific criteria. 
The script also includes functionality to print out monthly calendars with event counts.

Key Features:
1. Add events to a file with date, start time, end time, main message, and optional additional message.
2. Retrieve and print events based on specific search criteria, including date ranges and exact matches.
3. Print monthly calendars showing the number of events for each day in a given month and year.

Classes:
- DateDescriptor: A descriptor to validate and format date strings.
- TimeDescriptor: A descriptor to validate and format time strings.
- Organizer: Manages event storage and retrieval, and generates monthly calendars.

Usage:
- Create an instance of Organizer with a file name.
- Use the instance as a callable to add events.
- Call the instance with different parameters to retrieve or display events.
"""

import math

class DateDescriptor:
    def __get__(self, instance, owner):
        return instance._date

    def __set__(self, instance, value):
        try:
            day, month, year = value.split('/')
            day, month, year = int(day), int(month), int(year)
            if 1 <= day <= 31 and 1 <= month <= 12 and 0 < year:
                instance._date = f"{day:02d}/{month:02d}/{year:04d}"
            else:
                raise ValueError("Incorrect date format")
        except ValueError:
            raise ValueError("Incorrect date format")

    def __set_name__(self, owner, name):
        self.name = name
            
class TimeDescriptor:
    def __get__(self, instance, owner):
        return instance._time

    def __set__(self, instance, value):
        try:
            hour, minute, second = value.split(':')
            hour, minute, second = int(hour), int(minute), int(second)
            if 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60:
                instance._time = f"{hour:02d}/{minute:02d}/{second:02d}"
            else:
                raise ValueError("Incorrect time format")
        except ValueError:
            raise ValueError("Incorrect time format")

    def __set_name__(self, owner, name):
        self.name = name
            
class Organizer:
    date = DateDescriptor()
    time = TimeDescriptor()
    
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            with open(file_name, 'r') as file:
                pass
        except FileNotFoundError:
            with open(file_name, 'w') as file:
                pass
        
    def __call__(self, data, start_time=None, end_time=None, main_message=None, additional_message=None):
        if main_message is None:
            with open(self.file_name, 'r') as file:
                if start_time is None and len(data) == 10:
                    for line in file:
                        part = line[:len(line)-1].split(', ')
                        if data in line:
                            try:
                                print(f'{part[3]} ({part[4]})')
                            except IndexError:
                                print(part[3])
                elif start_time is not None and end_time is None:
                    for line in file:
                        part = line[:len(line)-1].split(', ')
                        if data in part[0]:
                            if start_time >= part[1] and start_time <= part[2]:
                                try:
                                    print(f'{part[3]} ({part[4]})')
                                except IndexError:
                                    print(part[3])
                elif end_time is not None:
                    for line in file:
                        part = line[:len(line)-1].split(', ')
                        if data in part[0]:
                            if (start_time >= part[1] and start_time <= part[2]) and (end_time >= part[1] and end_time <= part[2]):
                                try:
                                    print(f'{part[3]} ({part[4]})')
                                except IndexError:
                                    print(part[3])
                elif start_time is None and len(data) == 15:
                    data1, data2 = data.split(':')
                    month1, year1 = int(data1[0:2]), int(data1[3:])
                    month2, year2 = int(data2[0:2]), int(data2[3:])
                    month_range = month1
                    year_range = year1
                    max_lens = []
                    while True:
                        if month_range > month2 and year_range >= year2:
                            break
                        count = 0
                        max_lens.append(len(max(self.print_month(month_range, year_range)[8:], key=len)))
                        if month_range % 12 == 0:
                            year_range += 1
                            month_range = 0
                        month_range += 1
                    month_range = month1
                    year_range = year1
                    while True:
                        if month_range > month2 and year_range >= year2:
                            break
                        count = 0
                        max_len = max(max_lens)
                        print("{:^{}s}".format(self.print_month(month_range, year_range)[0], max_len * 4 + len(self.print_month(month_range, year_range)[0])), '\n')
                        for i in self.print_month(month_range, year_range)[1:]:
                            i = "{:^{}s}".format(i, max_len)
                            print(i, end=' ')
                            count += 1
                            if count == 7:
                                count = 0
                                print('\n')
                        if month_range % 12 == 0:
                            year_range += 1
                            month_range = 0
                        month_range += 1
                        print('\n\n')
        else:
            self.date = data
            self.time = start_time
            self.time = end_time
            with open(self.file_name, 'a') as file:
                if additional_message is not None:
                    file.write(f'{data}, {start_time}, {end_time}, {main_message}, {additional_message}\n')
                else:
                    file.write(f'{data}, {start_time}, {end_time}, {main_message}\n')
                    
    def print_month(self, month: int, year: int):
        day = 1
        y = year
        if month <= 2:
            day = 4
            y -= 1
        day_for_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        name_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day_for_month[2] = 29
        first_day = 1 + (day + y + y // 4 - y // 100 + y // 400 + (31 * month + 10) // 12) % 7
        list_month = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        if first_day != 1:
            for i in range(first_day - 1):
                list_month.append(' ')
        with open(self.file_name, 'r') as file:
            file_data = [i for i in file]
            count_all = 0
        for i in range(1, day_for_month[month] + 1):
            count = 0
            for line in file_data:
                if int(line[6:10]) == year and int(line[3:5]) == month and int(line[0:2]) == i:
                    count += 1
            count_all += count
            if count != 0:
                list_month.append(str(i) + str([count]))
            else:
                list_month.append(str(i))
        if count_all != 0:
            month_name = [name_month[month] + ' ' + str(year) + ' ' + '(' + str(count_all) + ')']
        else:
            month_name = [name_month[month] + ' ' + str(year)]
        return month_name + list_month

# Example usage
obj1 = Organizer("organizer.txt")
obj1('09/09/2023', '10:10:10', '')
obj1('09/2023:10/2024')


# In[ ]:




