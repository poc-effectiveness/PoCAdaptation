import re
import editdistance

if __name__ == "__main__":
    origin = """
    package edu.vision.se;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Test;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;

public class Testcase1 {

    private String _nestedDoc(int nesting, String open, String close, String content) {
        StringBuilder sb = new StringBuilder(nesting * (open.length() + close.length()));
        for (int i = 0; i < nesting; ++i) {
            sb.append(open);
            if ((i & 31) == 0) {
                sb.append("\n");
            }
        }
        sb.append("\n").append(content).append("\n");
        for (int i = 0; i < nesting; ++i) {
            sb.append(close);
            if ((i & 31) == 0) {
                sb.append("\n");
            }
        }
        return sb.toString();
    }

    @Test(timeout = 60000)
    public void testArrayWrapping() throws IOException {
        final String doc = _nestedDoc(9999, "[ ", "] ", "{}");
        try {
            ObjectMapper mapper = new ObjectMapper();
            mapper.readValue(doc, Object.class);
            fail("fail the test");
        } catch (JsonProcessingException e) {
            validateThrow(e);
        }
    }

    public void validateThrow(Throwable e) {
        assertTrue(e instanceof JsonProcessingException);
    }
}
    """
    
    valid = """
    package edu.vision.se;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Test;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;

public class Testcase1 {

    private String _nestedDoc(int nesting, String open, String close, String content) {
        StringBuilder sb = new StringBuilder(nesting * (open.length() + close.length()));
        for (int i = 0; i < nesting; ++i) {
            sb.append(open);
            if ((i & 31) == 0) {
                sb.append("\n");
            }
        }
        sb.append("\n").append(content).append("\n");
        for (int i = 0; i < nesting; ++i) {
            sb.append(close);
            if ((i & 31) == 0) {
                sb.append("\n");
            }
        }
        return sb.toString();
    }

    @Test(timeout = 60000)
    public void testArrayWrapping() throws IOException {
        final String doc = _nestedDoc(9999, "[ ", "] ", "{}");
        try {
            ObjectMapper mapper = new ObjectMapper();
            mapper.enable(com.fasterxml.jackson.core.JsonParser.Feature.STRICT_DUPLICATE_DETECTION);
            mapper.readTree(doc);
            fail("fail the test");
        } catch (StackOverflowError e) {
            // Expected in 2.12.5
            throw e;
        } catch (JsonProcessingException e) {
            validateThrow(e);
        }
    }

    public void validateThrow(Throwable e) {
        assertTrue(e instanceof JsonProcessingException);
    }
}
    """

    idea = origin

    # Calculate edit distance
    distance = editdistance.eval(origin, valid)
    print(f"Edit distance between the original and valid code: {distance}")
    distance = editdistance.eval(valid, idea)
    print(f"Edit distance between the valid and idea code: {distance}")
