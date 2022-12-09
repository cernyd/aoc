use std::{fs::File, io::BufReader, io::{BufRead, Lines}, collections::HashMap, cell::{RefCell}, rc::Rc};


#[derive(Debug)]
struct DirectoryFile {
    name: String,
    size: usize
}


#[derive(Debug)]
struct Directory<'a> {
    parent: Option<Rc<RefCell<Box<Directory<'a>>>>>,
    name: String,
    files: Vec<DirectoryFile>,
    directories: HashMap::<String, Rc<RefCell<Box<Directory<'a>>>>>
}


impl<'a> Directory<'a> {
    fn new(parent: Option<Rc<RefCell<Box<Directory<'a>>>>>, name: String) -> Rc<RefCell<Box<Directory>>> {
        return Rc::new(RefCell::new(Box::new(Directory {
            parent: parent,
            name: name,
            files: Vec::new(),
            directories: HashMap::new()
        })));
    }
}


#[derive(Debug)]
enum State {
    LoadNext,
    Seek,
    DirEntry,

    ChangeDir,
    ListDir
}


// From day 6
fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let file = File::open(path.as_ref()).expect("Unable to open file");
    let reader = BufReader::new(file);
    return reader.lines();
}


fn clone_parent(node: Rc<RefCell<Box<Directory>>>) -> Rc<RefCell<Box<Directory>>> {
    let parent = &node.borrow().parent;

    match parent {
        Some(x) => {
            return x.clone();
        },
        None => panic!()
    };
}


fn main() {
    let mut state = &State::LoadNext;
    let mut jump_to = &State::Seek;
    let mut lines = read_lines("filesys.txt").map(|line| line.unwrap());

    let mut root_dir = Directory::new(None, String::from("/"));
    let mut curdir = root_dir.clone();

    let mut line: String = String::new();
    loop {
        // println!("CURDIR: {:?}", curdir.borrow().name);

        match state {
            /* ----------------------------- Load next line ----------------------------- */
            State::LoadNext => {
                let line_value = lines.next();

                if line_value.is_none() {
                    println!("Last line reached, quitting");
                    break;
                }

                line = line_value.unwrap();
                state = jump_to;
            },
            /* ---------------------------- Seek next command --------------------------- */
            State::Seek => {
                if line.starts_with('$') {
                    match line.split(" ").nth(1).unwrap() {
                        "cd" => {
                            state = &State::ChangeDir;
                        },
                        "ls" => {
                            state = &State::LoadNext;
                            jump_to = &State::ListDir;
                        },
                        _ => ()
                    }
                }
            },
            /* ---------------------------- Change directory ---------------------------- */
            State::ChangeDir => {
                let target_dir = line.split(" ").nth(2).unwrap();
                match target_dir {
                    "/" => {
                        curdir = root_dir.clone();
                    },
                    ".." => {
                        curdir = clone_parent(curdir.clone());
                    },
                    _ => {
                        if !curdir.borrow().directories.contains_key(target_dir) {
                            let new_dir = Directory::new(Some(curdir.clone()), String::from(target_dir));

                            curdir.borrow_mut().directories.insert(
                                String::from(target_dir), new_dir
                            );
                        }

                        curdir = curdir.clone().borrow_mut().directories[target_dir].clone();
                    }
                }

                state = &State::LoadNext;
                jump_to = &State::Seek;
            },
            /* ----------------------------- List directory ----------------------------- */
            State::ListDir => {
                state = &State::LoadNext;
                jump_to = &State::ListDir;

                match line.chars().nth(0).unwrap() {
                    '$' => {
                        state = &State::Seek;
                    },
                    '0'..='9' => {
                        let filesize = line.split(" ").nth(0).unwrap().parse::<usize>().expect("Failed to parse filesize");
                        let filename = line.split(" ").nth(1).unwrap();

                        curdir.borrow_mut().files.push(
                            DirectoryFile { name: String::from(filename), size: filesize }
                        );
                    },
                    // 'd' => {
                    //     println!("-> directory! {line}");
                    // },
                    _ => ()
                };
            },
            _ => {
                panic!("Unimplemented state '{state:?}'");
            }
        }
    }
}
