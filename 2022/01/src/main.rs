// https://adventofcode.com/2022/day/1
use std::fs::File;
use std::io::{self, BufRead};


fn main() {
    let filename = "calories.txt";
    println!("Using file '{filename}'");

    // Setup file read
    let file = File::open(filename).expect(&format!("Failed to open file '{filename}'").to_string());
    let reader = io::BufReader::new(file);

    let mut max_calories: i64 = 0;
    if let Ok(lines) = Ok::<std::io::Lines<io::BufReader<File>>, String>(reader.lines()) {
        let mut current_calories: i64 = 0;
        // Iterate over calorie lines
        for line in lines {
            if let Ok(line_value) = line {
                // Compare current max with new value, zero current calories
                if line_value.is_empty() {
                    if current_calories > max_calories {
                        max_calories = current_calories;
                    }
                    current_calories = 0;
                // Add calories
                } else {
                    current_calories += line_value.parse::<i64>().unwrap();
                }
            }
        }
    }

    println!("Maximum elf calories: {max_calories} calories");
}
