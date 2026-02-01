// src/rust_core.rs
//
// High-Performance Intelligence Extraction Module
// Designed to be compiled as a Python Extension using PyO3 or loaded as a shared library.
//
// Usage Concept:
// import rust_core
// extracted = rust_core.extract_intelligence(text)

use regex::Regex;
use std::collections::HashMap;

// Pre-compiled regex patterns (lazy_static or once_cell would be used in production)
// For this draft, we define the logic structure.

pub struct Extractor {
    upi_regex: Regex,
    phone_regex: Regex,
    link_regex: Regex,
}

impl Extractor {
    pub fn new() -> Self {
        Extractor {
            upi_regex: Regex::new(r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}").unwrap(),
            phone_regex: Regex::new(r"(\+91[\-\s]?)?(91)?\d{10}").unwrap(),
            link_regex: Regex::new(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+").unwrap(),
        }
    }

    pub fn extract(&self, text: &str) -> HashMap<String, Vec<String>> {
        let mut results = HashMap::new();

        // High-speed UPI check
        let upi_matches: Vec<String> = self.upi_regex.find_iter(text)
            .map(|m| m.as_str().to_string())
            .collect();
        if !upi_matches.is_empty() {
            results.insert("upiIds".to_string(), upi_matches);
        }

        // High-speed Phone check
        let phone_matches: Vec<String> = self.phone_regex.find_iter(text)
            .map(|m| m.as_str().to_string())
            .collect();
        if !phone_matches.is_empty() {
            results.insert("phoneNumbers".to_string(), phone_matches);
        }

        // High-speed Link check
         let link_matches: Vec<String> = self.link_regex.find_iter(text)
            .map(|m| m.as_str().to_string())
            .collect();
        if !link_matches.is_empty() {
             results.insert("phishingLinks".to_string(), link_matches);
        }

        results
    }
}

// Entry point for testing this module independently
fn main() {
    let extractor = Extractor::new();
    let text = "Pay me at scammer@sbi or call +91-9876543210. Visit http://evil.com";
    let intel = extractor.extract(text);
    println!("Extracted Intelligence: {:?}", intel);
}
