#![allow(dead_code)]
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader, Lines};


struct RucksackIterator {
    lines: Lines<BufReader<File>>
}


impl RucksackIterator {
    fn new<T: AsRef<str>>(path: T) -> RucksackIterator {
        return RucksackIterator {lines: read_lines(path)};
    }
}


impl Iterator for RucksackIterator {
    type Item = Rucksack;

    fn next(&mut self) -> Option<Self::Item> {
        let next_line = self.lines.next();

        if next_line.is_none() {
            return None;
        } else {
            return Some(Rucksack { contents: next_line.unwrap().expect("Failed to fetch line") });
        }
    }
}

struct Rucksack {
    contents: String
}


impl Rucksack {
    fn first_half(&self) -> String {
        return String::from(&self.contents[..&self.contents.len()/2]);
    }

    fn second_half(&self) -> String  {
        return String::from(&self.contents[&self.contents.len()/2..]);
    }

    fn duplicates(&self) -> Vec::<char> {
        let mut values = HashSet::<char>::new();
        let mut duplicates = Vec::<char>::new();

        for ch in self.first_half().chars() {
            values.insert(ch);
        }

        for ch in self.second_half().chars() {
            if values.contains(&ch) {
                duplicates.push(ch);
                values.remove(&ch);
            }
        }

        return duplicates;
    }

    fn len(&self) -> usize {
        return self.contents.len();
    }
}

fn duplicate_priority(ch: char) -> i32 {
    // Lowercase ASCII
    if ch >= 'a' {
        return ch as i32 - 'a' as i32 + 1;
    // Uppercase ASCII
    } else {
        return ch as i32 - 'A' as i32 + 26 + 1;
    }
}

fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let path_str = path.as_ref();
    let file = File::open(path_str).expect(
        format!("Failed to open file '{path_str}'").as_str()
    );
    let reader = BufReader::new(file);

    return reader.lines();
}

fn main() {
    let mut values = Vec::<char>::new();

    for line in RucksackIterator::new("rucksacks.txt") {
        // println!("Line '{}' (len {})", line.contents, line.len());
        // println!("First half '{}' second half '{}'", line.first_half(), line.second_half());

        for dup in line.duplicates() {
            // println!("Dupe: {dup}");
            values.push(dup);
        }
    }

    let mut total_priorities = 0;
    for value in values {
        let prio = duplicate_priority(value);
        // println!("Value: {value} (priority {prio})");
        total_priorities += prio;
    }

    println!("Total priority: {total_priorities}");
}
