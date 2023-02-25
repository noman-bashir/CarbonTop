package com.carbontop.readCarbonCsv;

import java.io.FileReader;
import java.io.IOException;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import com.opencsv.CSVReader;


@RestController
public class Userdemo {
    private static final String CSV_FILE_PATH = "data/US-MIDW-MISO.csv";

    @GetMapping("/datetime/{datetime}")
    public ResponseEntity<String> getClosestValue(@PathVariable String datetime) {
        
        datetime = datetime.replace(" ", "+");
        DateTimeFormatter formatter = DateTimeFormatter.ISO_OFFSET_DATE_TIME;
        ZonedDateTime d = ZonedDateTime.parse(datetime,formatter);

        // Step 3: Load the CSV file into memory using OpenCSV
        List<String[]> rows = null;
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        try (CSVReader reader = new CSVReader(new FileReader(CSV_FILE_PATH))) {
            rows = reader.readAll();
        } catch (IOException e) {
            System.out.println(System.getProperty("user.dir"));
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error reading CSV file:" + e);

        }

        // Step 4: Binary Search to get latest lower value
        String carbonValue = null;

        int l=1,h=rows.size()-1;
        while(l<=h)
        {
            int mid = (l+h)/2;
            String[] row = rows.get(mid);
            ZonedDateTime d2 = ZonedDateTime.parse(row[0]);
            //mid is <= currr && mid+1>curr
            System.out.println(l+":"+h+":"+mid+":"+d2);
            if(mid == rows.size()-1 || (Duration.between(d2, d).toMillis() >=0 && Duration.between(ZonedDateTime.parse(rows.get(mid+1)[0]), d).toMillis() <0))
            {
                carbonValue = row[5];
                break;
            }
            else if(Duration.between(d2, d).toMillis() < 0)
                h = mid-1;
            else
                l = mid+1;
            
        }

        if (carbonValue == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("No matching value found");
        } else {
            return ResponseEntity.ok(carbonValue);
        }
    }
}
