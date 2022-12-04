use std::{io::{BufReader, BufRead, Lines}, fs::File};


fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let path_str = path.as_ref();
    let file = File::open(path_str).expect(
        format!("Failed to open file '{path_str}'").as_str()
    );
    let reader = BufReader::new(file);
    return reader.lines();
}


fn section_range(section: &str) -> Vec::<i32> {
    return Some(section.split("-").map(|num|
        if let Ok(result) = num.parse::<i32>() {
            return result;
        } else {
            panic!("Unable to parse number");
        }
    )).expect("Failed to parse section").collect();
}


// Does s1 contain s2?
fn does_contain(s1_start: i32, s1_end: i32, s2_start: i32, s2_end: i32) -> bool {
    return s1_start <= s2_start && s1_end >= s2_end;
}

// If a is between b and c
fn in_range(a: i32, b: i32, c: i32) -> bool {
    return b <= a && a <= c;
}

// Does s1 overlap with s2?
fn does_overlap(s1_start: i32, s1_end: i32, s2_start: i32, s2_end: i32) -> bool {
    return in_range(s1_start, s2_start, s2_end) || in_range(s1_end, s2_start, s2_end);
}

fn overlap_check(section: &str, total_overlap: bool) -> bool {
    let sections: Vec<_> = section.split(",").collect();
    let section_1 = section_range(sections[0]);
    let section_2 = section_range(sections[1]);

    let s1_start = section_1[0];
    let s1_end = section_1[1];

    let s2_start = section_2[0];
    let s2_end = section_2[1];

    let mut result = does_contain(s1_start, s1_end, s2_start, s2_end) ||
                           does_contain(s2_start, s2_end, s1_start, s1_end);

    if total_overlap {
        return result;
    }

    result = result || does_overlap(s1_start, s1_end, s2_start, s2_end) ||
                       does_overlap(s2_start, s2_end, s1_start, s1_end);

    return result;
}


fn get_overlaps(lines: Lines<BufReader<File>>, total_overlap: bool) -> i32 {
    return lines.map(
        |line|
        if let Ok(line_value) = line {
            return overlap_check(&line_value, total_overlap) as i32;
        } else {
            panic!();
        }
    ).sum::<i32>();
}


fn main() {
    let total_overlaps = get_overlaps(read_lines("assignments.txt"), true);
    let any_overlaps = get_overlaps(read_lines("assignments.txt"), false);

    println!("Total overlaps: {total_overlaps}");
    println!("Any overlaps: {any_overlaps}");
}
