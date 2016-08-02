import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.util.List;

/**
 * Created by vsinevic on 14.07.2016.
 */
public class Line {
    private List<Position> positions;
    public Line(List<Position> positions) {
        this.positions = positions;
    }
    public String toJson() {
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);
            String json = objectMapper.writeValueAsString(this);
            System.out.println("line converted to json\n");
            return json;
        } catch (JsonProcessingException e) {
            System.out.println(e.getMessage());
        }
        System.out.println("line not converted to jsonn");
        return "";
    }

    public int length() {
        return positions.size();
    }

    public Position getByIndex(int index) {
        return positions.get(index);
    }
}
