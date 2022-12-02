use core::panic;
use std::io::{self, BufRead};
use std::fs::File;


// Returns an iterator of lines from a target file
fn read_lines(filename: &str) -> std::io::Lines<io::BufReader<File>> {
    let file = File::open(filename).expect(
        &mut format!("Failed to open file '{filename}'").to_string()
    );

    let reader = io::BufReader::new(file);

    return reader.lines();
}

fn shape_name(ch: char) -> String {
    let name = match ch {
        'A' | 'X' => "Rock",  // Rock
        'B' | 'Y' => "Paper",  // Paper
        'C' | 'Z' => "Scissors",  // Scissors
        _ => panic!("{}", format!("Unknown value {}", ch).to_string())
    };

    return String::from(name);
}

fn outcome_name(ch: char) -> String {
    let name = match ch {
        'A' | 'X' => "Lose",
        'B' | 'Y' => "Draw",
        'C' | 'Z' => "Win",
        _ => panic!("{}", format!("Unknown value {}", ch).to_string())
    };

    return String::from(name);
}

// Returns the score value of a sign
fn shape_value(ch: char) -> i32 {
    return match ch {
        'A' | 'X' => 1,  // Rock
        'B' | 'Y' => 2,  // Paper
        'C' | 'Z' => 3,  // Scissors
        _ => panic!("{}", format!("Unknown value {}", ch).to_string())
    };
}

// Returns true if value B beats value A
fn did_win(a: char, b: char) -> bool {
    return match b {
        'X' => a == 'C',  // Rock beats scissors
        'Y' => a == 'A',  // Paper beats rock
        'Z' => a == 'B',  // Scissors beat paper
        _ => false
    };
}

fn outcome_shape(a: char, outcome: char) -> char {
    return match outcome {
        'X' =>  // To lose
            match a {
                'A' => 'Z',  // Rock beats scissors
                'B' => 'X',  // Paper beats rock
                'C' => 'Y',  // Scissors beat paper
                _ => panic!("Unknown symbol")
            },
        'Y' =>  // To draw
            match a {
                'A' => 'X',
                'B' => 'Y',
                'C' => 'Z',
                _ => panic!("Unknown symbol")
            }
        'Z' =>  // To win
            match a {
                'A' => 'Y',  // Paper beats rock
                'B' => 'Z',  // Scissors beat paper
                'C' => 'X',  // Rock beats scissors
                _ => panic!("Unknown symbol")
            }
        _ => panic!("Unknown symbol")
    };
}

fn is_draw(a: char, b: char) -> bool {
    return (a == 'A' && b == 'X') || (a == 'B' && b == 'Y') || (a == 'C' && b == 'Z');
}

// If target_outcome = false, the second character is treated as the symbol that needs to be played
// If target_outcome = true, the second character is treated as the outcome that needs to happen
fn round_score(line: &String, target_outcome: bool) -> i32 {
    assert!(line.len() >= 2);
    let a = line.chars().nth(0).unwrap();
    let mut b = line.chars().nth(2).unwrap();

    println!();
    // Change the second character to get desired round result
    if target_outcome {
        println!("\n{a} ({}) -> outcome {b} ({})", shape_name(a), outcome_name(b));
        b = outcome_shape(a, b);
    }

    let b_value = shape_value(b);

    let mut score = b_value;

    println!("{a} ({}) -> {b} ({})", shape_name(a), shape_name(b));
    println!("{} -> {}", shape_value(a), shape_value(b));
    if did_win(a, b) {
        score += 6;
    } else if is_draw(a, b) {
        score += 3;
    }
    println!("Score: {score}");

    return score;
}


fn main() {
    let filename = "strategy.txt";

    let mut total_score: i32 = 0;
    for (_, line) in read_lines(filename).enumerate() {
        let line_values = line.unwrap();

        let score = round_score(&line_values, true);
        total_score += score;
    }
    println!("Total score: {total_score}");
}
