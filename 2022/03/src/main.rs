#![allow(dead_code)]
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader, Lines};

/* ---------------------------- RucksackIterator ---------------------------- */

// Iterates individual rucksacks from the input file
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

/* -------------------------------- Rucksack -------------------------------- */

struct Rucksack {
    contents: String
}


impl Rucksack {
    // Gets first half of the rucksack
    fn first_half(&self) -> String {
        return String::from(&self.contents[..&self.contents.len()/2]);
    }

    // Gets second half of the rucksack
    fn second_half(&self) -> String  {
        return String::from(&self.contents[&self.contents.len()/2..]);
    }

    // Finds values duplicate between rucksack parts
    fn duplicates(&self) -> Vec::<char> {
        let mut values = HashSet::<char>::new();
        let mut duplicates = Vec::<char>::new();

        // Insert first half
        for ch in self.first_half().chars() {
            values.insert(ch);
        }

        // Check if values from second half are not in first half
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

// Returns the priority value of characters a-z A-Z
fn duplicate_priority(ch: char) -> i32 {
    // Lowercase ASCII
    if ch >= 'a' {
        return ch as i32 - 'a' as i32 + 1;
    // Uppercase ASCII
    } else {
        return ch as i32 - 'A' as i32 + 26 + 1;
    }
}

// Returns an iterator for lines from the input file
fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let path_str = path.as_ref();
    let file = File::open(path_str).expect(
        format!("Failed to open file '{path_str}'").as_str()
    );
    let reader = BufReader::new(file);

    return reader.lines();
}

fn main() {
    // Duplicate values in rucksack halves
    let mut duplicates = Vec::<char>::new();
    // Items common amongst one group (of 3 elves)
    let mut group_common = HashSet::<char>::new();
    // Badges for each group
    let mut group_badges = Vec::<char>::new();
    // Total number of groups
    let mut group_count = 0;

    // Iterate over rucksacks
    for line in RucksackIterator::new("rucksacks.txt") {
        // println!("Line '{}' (len {})", line.contents, line.len());
        // println!("First half '{}' second half '{}'", line.first_half(), line.second_half());

        // Find duplicates for part 1
        for dup in line.duplicates() {
            // println!("Dupe: {dup}");
            duplicates.push(dup);

        }

        // If first group, insert all unique items in rucksack
        if group_count == 0 {
            for ch in line.contents.chars() {
                group_common.insert(ch);
            }
        // If other elves in group (second and third), find values common for
        // this elf and the previous elves
        } else {
            let mut new_common = HashSet::<char>::new();

            // Add common values
            for ch in line.contents.chars() {
                if group_common.contains(&ch) {
                    new_common.insert(ch);
                }
            }

            // Update the common values
            group_common.clear();
            group_common.extend(new_common);
        }

        // Debug print
        // print!("Common: ");
        // for ch in group_common.iter() {
        //     print!("{ch}");
        // }
        // println!();

        group_count += 1;
        // Add badge and clear temp variables at the end of group
        if group_count % 3 == 0 {
            group_count = 0;

            // There can only be one badge
            assert_eq!(group_common.len(), 1);
            for badge in group_common.iter() {
                group_badges.push(*badge);
            }
            group_common.clear();
            // println!("=== GROUP END ===");
        }
    }

    let mut total_priorities = 0;
    for value in duplicates {
        let prio = duplicate_priority(value);
        // println!("Value: {value} (priority {prio})");
        total_priorities += prio;
    }

    let mut group_badge_priorities = 0;
    for badge in group_badges {
        // println!("Badge: {badge}");
        group_badge_priorities += duplicate_priority(badge);
    }

    println!("Total priority: {total_priorities}");
    println!("Group badge priorities: {group_badge_priorities}");
}
