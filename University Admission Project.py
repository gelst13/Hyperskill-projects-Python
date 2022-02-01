# University Admission Procedure project
"""Program that creates the admission lists to for enrolling based on mean score and
result of special exam."""
import pandas as pd
from pandas.core.common import SettingWithCopyWarning


class Admission:
    """Create the Admission object and related functionality."""

    def __init__(self):
        """The initializer for the class.

        Arguments:
        n -- integer: maximum number of students for each department.
        df -- DataFrame, created from file with applicants' data.
        accepted -- dictionary: like {'department': [applicants]}, stores data
        about accepted (successful) applicants
        start_next_round -- Bool: flag to start/cancel next round of Admission
        dep_limits -- dictionary: like {'department': integer}, stores
        calculated number of available places on each department
        priority -- integer: ordinal number of priority (1st, 2nd, 3d) in df."""

        self.n = 7
        self.df = None
        self.accepted = {}
        self.start_next_round = False
        self.dep_limits = {}
        self.priority = 0  # 1 = 'A_priority', 2 = 'B_priority', 3 = 'C_priority'

    departments = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']

    def run(self):
        """Chief method of the Enrollment class."""

        Admission.define_limit(self)
        Admission.create_df(self)
        # Admission.df_info(self)
        for priority in range(1, 4):
            print(f'Start round{priority}')
            Admission.df_info(self)  # show df.shape in the beginning and in the end of round
            self.priority = priority  # !! it was a number of needed column in previous df
            if priority == 1:
                Admission.round1(self)
                data = self.accepted
                Admission.remove_accepted(self, data)
            else:
                print('check_available_places')
                if Admission.check_available_places(self):
                    self.dep_limits = Admission.compute_round2_limits(self)
                    data = Admission.round2(self)
                    # print(data)
                    Admission.remove_accepted(self, data)
                    Admission.add_new_to_accepted(self, data)
                    self.start_next_round = False
        # Admission.print_result(self)
        Admission.save_result(self)
        print('Admission procedure is finished. The results(admission lists) are saved in files.')


    def define_limit(self):
        self.n = int(input('Enter the maximum number of students for a department: '))

    def create_df(self):
        """Create df from file - applicant_list_7.txt and save it into self.df"""

        columns = ['Name', 'Last name', 'physics', 'chemistry', 'math', 'comp sc', 'special',
                   'A_priority', 'B_priority', 'C_priority']
        df = pd.read_csv('applicant_list_7.txt', sep=' ', names=columns)
        df.index.name = 'Index'
        # print(df.head(1))
        self.df = df

    def df_info(self):
        """Show original df info like df.shape and etc."""

        print('original db:')
        print(self.df.head(10))
        print(self.df.shape)
        # print(self.df.A_priority.value_counts())

    def select_from_df(self, priority, department):
        """Supporting method for create_list_dep().

        Create and return slice of dataframe with applicants for a department,
        depending on chosen priority of admission procedure.
        columns=['Name', 'Last name', 'special','finals']."""

        # Some departments need several exams. We calculate the mean score to rank the applicants
        # in exams Dictionary values are the names of columns from self.df, keys are departments
        exams = {'Biotech': ('chemistry', 'physics'), 'Chemistry': ('chemistry',),
                 'Engineering': ('comp sc', 'math'), 'Mathematics': ('math',),
                 'Physics': ('physics', 'math')}

        df_new = Admission.insert_priority(self, priority, department)
        try:
            # create slice of df for departments that need only 1 final exam
            if len(exams[department]) == 1:
                df_ = df_new[['Name', 'Last name', 'special', exams[department][0]]]
                df_['special'] = df_['special'].astype(float)  # convert integer values into float
                #  create column 'finals' from column with exam result:
                df_.rename(columns={f'{exams[department][0]}': 'finals'}, inplace=True)
                df_['finals'] = df_['finals'].astype(float)  # convert integer values into float
            else:
                # create slice of df for departments that need mean score for 2 final exams
                df_ = df_new[['Name', 'Last name', 'special', exams[department][0], exams[department][1]]]
                df_['special'] = df_['special'].astype(float)   # convert integer values into float
                # create column 'finals' and fill it with mean score for 2 final exams:
                df_['finals'] = round((df_[exams[department][0]] + df_[exams[department][1]])/2, 1)
                # delete unnecessary columns from df-slice:
                df_.drop(columns=[exams[department][0], exams[department][1]], inplace=True)
            return df_
        except SettingWithCopyWarning as e:
            print(e)

    def create_list_dep(self, priority, department):
        """Create and return list of applicants for a department,
        depending on chosen priority of admission procedure.

        [Name, Surname, max(special, final/mean score), index from original df]"""

        df_ = Admission.select_from_df(self, priority, department)
        applicants = []
        for array in df_.values:
            applicants.append([array[0], array[1], max(array[2], array[3])])

        if not applicants:
            return []

        indices = []
        for index in df_.index:
            indices.append(index)
        for number in range(len(indices)):
            applicants[number].append(indices[number])
        return applicants

    def insert_priority(self, priority, department):
        """ Supporting method for create_list_dep().
        Return selection of rows(for a department)& columns(for a priority)."""

        if priority == 1:
            df_loc_priority = self.df.loc[self.df.A_priority == department, 'Name':'special']
        elif priority == 2:
            df_loc_priority = self.df.loc[self.df.B_priority == department, 'Name':'special']
        elif priority == 3:
            df_loc_priority = self.df.loc[self.df.C_priority == department, 'Name':'special']
        return df_loc_priority

    @staticmethod
    def sort_applicants(data: list):
        """Sort the list of applicants by exam results - desc.
        Return [Name, Surname, exam result, index from original df]"""

        data_sorted = sorted(data, key=lambda x: (-float(x[2]), x[0], x[1]))
        return data_sorted


    def round1(self):
        """Rank and choose N-best applicants for admission.
        Save applicants' data in self.accepted."""

        priority = self.priority
        for department in Admission.departments:
            self.accepted[department] = []
            applicants = Admission.create_list_dep(self, priority, department)
            applicants_sorted = Admission.sort_applicants(applicants)
            if len(applicants_sorted) <= self.n:  # i.e. <= limit
                self.accepted[department] = applicants_sorted
            else:
                self.accepted[department] = applicants_sorted[:self.n]
            # print(self.accepted[department][:3])

    def round2(self):
        """Rank and choose applicants to accept in case of next rounds of admission.
        Return dictionary like {'department': [applicants]}."""

        priority = self.priority
        accepted_new = {}
        print(self.dep_limits)  # output how much places are there for the next round of admission
        for dep in self.dep_limits.keys():
            if self.dep_limits[dep] > 0:
                # print(dep)
                n = self.dep_limits[dep]
                accepted_new[dep] = []
                applicants = Admission.create_list_dep(self, priority, dep)
                applicants_sorted = Admission.sort_applicants(applicants)
                accepted_new[dep] = applicants_sorted[:n]
                # print(dep, applicants_sorted[:n])
        return accepted_new

    def add_new_to_accepted(self, data):
        """Add in self.accepted successful applicants from round 2/round3."""

        to_accept = data
        for dep in list(self.accepted.keys()):
            try:
                self.accepted.update({dep: (self.accepted[dep] + to_accept[dep])})
            except KeyError:
                continue

    @staticmethod
    def find_index_to_delete(data):
        """Supporting method for remove_accepted().
        Return list of indices for rows to delete from original df."""

        index_to_delete = []
        to_delete = data  # dictionary like {'department': [applicants]}
        for dep in list(to_delete.keys()):  # to_delete.keys() = list of 'department's
            for applicant in to_delete[dep]:
                index_to_delete.append(applicant[3])
        return index_to_delete


    def remove_accepted(self, data):
        """Delete rows with accepted applicants from original df"""

        accepted = data  # dictionary like {'department': [applicants]}
        indices = Admission.find_index_to_delete(accepted)
        self.df.drop(index=indices, inplace=True)
        # print(self.df.shape)

    def check_available_places(self):
        """Return flag to start/cancel next round of admission. Change to True
        self.start_next_round if find any remaining places in departments."""

        for department in self.accepted.keys():
            # print(department, len(self.accepted[department]) < self.n)
            if len(self.accepted[department]) < self.n:
                self.start_next_round = True
        return self.start_next_round

    def compute_round2_limits(self):
        """Return dictionary like {'department': integer}, that stores
        calculated number of available places on each department."""

        dep_limits = {}
        for dep in list(self.accepted.keys()):
            dep_limits[dep] = self.n - len(self.accepted[dep])
        return dep_limits

    def print_result(self):
        """Print the departments in the alphabetic order, output the names and
        the mean score of enrolled applicants for each department"""

        # print('Admission results:')
        for dep in sorted(list(self.accepted.keys())):
            print(dep)
            for applicant in sorted(self.accepted[dep], key=lambda x: (-float(x[2]), x[0], x[1])):
                print(*applicant[:3], sep=' ')
            print()


    def save_result(self):
        for department in sorted(list(self.accepted.keys())):
            with open(f"{department.lower()}.txt", 'w', encoding='utf-8') as f:
                for applicant in sorted(self.accepted[department], key=lambda x: (-float(x[2]), x[0], x[1])):
                    del applicant[3]
                    f.write(' '.join(map(lambda x: str(x), applicant)) + '\n')


new = Admission()
Admission.run(new)
