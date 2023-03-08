import json
from abc import ABC, abstractmethod

def text_create(path, content=''):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def text_read(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

def make_json(dic, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(dic, f, indent=2)
        f.close()

def open_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        contents = json.load(f)
        f.close()
    return contents

# I wish this supported storage of nested objects
class PersistenceABC(ABC):
    """Handles saving to and loading from a file

    Note from myself to myself after using this:
    --
    on init -- need to call super().__init__(path)

    Arguments:
    --
    path -- the file where a description of your object is stored (for implement_filedata)

    Abstract methods:
    --
    object_to_filedata() -- Should return something that you can put into a file. (for saving)
    implement_filedata(filedata) -- Use data (like a dict or string or list) to edit/create/etc, the object. (for loading)

    Will grant you these methods:
    --
    save() -- Store the current state of the object in self.path
    load() -- Get data from self.path and implement it

    Dependencies
    --
    text_create(path, content)
    text_read(path)
    make_json(dic_or_list, path)
    open_json(path)
    """

    def __init__(self, path):
        """Set path, saver and loader"""

        self.path = path
        self.ext = path.split('.')[-1]
        
        # set saver and loader
        if self.ext == 'txt':
            self._saver = self._save_txt
            self._loader = self._load_txt
        elif self.ext == 'json':
            self._saver = self._save_json
            self._loader = self._load_json
        else:
            raise ValueError(f'extension must be txt or json, but path is {path}')

    # Set these to be allowed to use this class.

    @abstractmethod
    def object_to_filedata(self):
        """Should return something that you can put into a file. (for saving)"""
        pass
    @abstractmethod
    def implement_filedata(self, filedata):
        """Use data (like a dict or string or list) to edit/create/etc, the object. (for loading)"""
        pass

    # internal methods

    ## save to self.path
    def _save_txt(self, contents):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(contents)
    def _save_json(self, contents):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(contents, f, indent=2)

    ## load from self.path
    def _load_txt(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            contents = f.read()
        return contents
    def _load_json(self):
        with open(self.path, 'r', encoding="utf-8") as f:
            contents = json.load(f)
        return contents

    # external methods

    def save(self):
        """Store the current state of the object in self.path"""
        filedata = self.object_to_filedata()
        self._saver(filedata)

    def load(self):
        """Get data from self.path and implement it"""
        filedata = self._loader()
        self.implement_filedata(filedata)

# example use of PersistenceABC, with the gpt-3.5-turbo chatbot
class ChatbotStorage(PersistenceABC):
    """Handles saving and loading of a single chatbot."""

    def __init__(self, path, chatbot_object):
        self.path = path
        self.chatbot_object = chatbot_object

        super().__init__(path)

    def implement_filedata(self, list_of_dicts):
        """Add messages one by one, from the list of dictionaries.
        
        Example argument:
        list_of_dicts = [
            {
                'role': 'system',
                'content': 'You are a terrible chatbot.',
            },
            {
                'role': 'user',
                'content': 'can you help me with something?',
            },
            {
                'role': 'assistant',
                'content': 'No, hahaha get rekt.',
            },
        ]
        """

        lod = list_of_dicts

        # validating
        assert type(lod) is list
        for item in lod:
            assert type(item) is dict
            for key in ('role','content'):
                assert key in item
            assert item['role'] in ('system','assistant','user')

        # adding messages
        for item in lod:
            self.chatbot_object.add_message(
                item['role'],
                item['content'],
            )
    
    def object_to_filedata(self):
        """Just returns chatbot_object.context"""

        lod = self.chatbot_object.context  # list of dicts
        # validating
        assert type(lod) is list
        for item in lod:
            assert type(item) is dict
            for key in ('role','content'):
                assert key in item
            assert item['role'] in ('system','assistant','user')
        return lod



class QaStorage(PersistenceABC):
    def __init__(self, path, data_handler):
        super().__init__(path)

        self.data_handler = data_handler
    
    def _validate_data(self, data):
        # validate
        assert type(data) is list
        for item in data:
            assert type(item) is dict
            for key in ('question', 'answer'):
                assert key in item

    def object_to_filedata(self):
        """This should enable saving, by just returning the data object."""
        data = self.data_handler.data
        self._validate_data(data)
        return data

    def implement_filedata(self, filedata):
        """This should enable loading, by just setting data to filedata, which if validated is a list of dictionaries."""
        self._validate_data(filedata)
        self.data_handler.data = filedata

class QaHandler:
    def __init__(self, path):
        self.path = path
        self.storage = QaStorage(path, self)

        self.storage.load()
        print('  (loaded upon starting)  ')

    # case insensitive search
    def search(self, term):
        term = term.lower()
        findings = []
        qa = self.data
        for d in qa:
            q = d['question'].lower()
            a = d['answer'].lower()
            if term in q or term in a:
                # hotfix of duplicate questions and answers
                if d in findings:
                    continue
                    
                findings.append(d)
        return findings

    def add_qa(self, q, a):
        for item in self.data:
            if item['question'] == q:
                print('  (q already exists, not adding anything.)  ')
                return 'this already exists.'

        self.data.append({
            'question':q,
            'answer':a,
        })
        self.storage.save()
        print('  (added data and saved.)  ')
        return 'added successfully'
    
    def delete_q(self, q):
        new_data = []
        removed_pairs = []
        for item in self.data:
            if item['question'] == q:
                removed_pairs.append(item)
                continue
            new_data.append(item)
        self.data = new_data
        self.storage.save()
        print('  (saved after deleting pairs)  ')
        return removed_pairs
